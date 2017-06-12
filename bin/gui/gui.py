import os
import sys
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import simpledialog
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import OrderedDict
from viewer import Viewer
from collection_manager import CollectionManager
sys.path.insert(0, os.path.abspath("../.."))
from specdal.spectrum import Spectrum
from specdal.collection import Collection
from specdal import readers as r

class Session(tk.Tk):
    def __init__(self, parent):
        self.collections = OrderedDict()
        self.create_gui(parent)

    def create_gui(self, parent):
        self.mw = parent
        h = self.mw.winfo_screenheight()
        w = self.mw.winfo_screenwidth()
        self.mw.geometry("%dx%d+0+0" % (w, h))

        self.collection_manager = CollectionManager(self.mw)
        self.collection_manager.grid(row=1, column=0,
                                     sticky=tk.N+tk.S)

        self.viewer = Viewer(self.mw)
        self.viewer.grid(row=1, column=1)

        # for testing purposes
        tk.Button(self.mw, text="plot", command = lambda : self.plot()).grid(column=0)
        tk.Button(self.mw, text="read test", command = lambda : self.test_read()).grid(column=0)
        tk.Button(self.mw, text="read directory", command = lambda : self.read_dir()).grid(column=0)
        tk.Button(self.mw, text="read files", command = lambda : self.read_files()).grid(column=0)
        tk.Button(self.mw, text="group by", command = lambda : self.groupby()).grid(column=0)
        tk.Button(self.mw, text="resample", command = lambda : self.resample()).grid(column=0)
        tk.Button(self.mw, text="stitch", command = lambda : self.stitch()).grid(column=0)
        tk.Button(self.mw, text="jump_correct",
                  command = lambda : self.jump_correct()).grid(column=0)
        tk.Button(self.mw, text="remove selection",
                  command = lambda : self.remove_selection()).grid(column=0)

    def remove_selection(self):
        selections = self.collection_manager.get_selection()
        for coll_name, spec_name in selections:
            if spec_name is None:
                self.collection_manager.remove_collection(coll_name)
            else:
                collection = self.collections[coll_name]
                collection.remove_spectrum(spec_name)
                self.collection_manager.update(coll_name)
        self.viewer.update()
        
    def resample(self):
        selections = self.collection_manager.get_selection()
        for coll_name, spec_name in selections:
            collection = self.collections[coll_name]
            if spec_name is None:
                collection.resample()
            else:
                spectrum = collection.get_spectrum(spec_name).resample()
        self.viewer.update()

    def stitch(self):
        selections = self.collection_manager.get_selection()
        for coll_name, spec_name in selections:
            collection = self.collections[coll_name]
            if spec_name is None:
                collection.stitch()
            else:
                spectrum = collection.get_spectrum(spec_name).stitch()
        self.viewer.update()

    def jump_correct(self):
        splices = simpledialog.askstring(title="Jump correction",
                                         prompt="Enter splices (i.e. 1000, 1800):",
                                         initialvalue="1000, 1800")
        splices = list(map(int, splices.replace(" ", "").split(","))) # convert to list

        reference = simpledialog.askinteger(title="Jump correction",
                                            prompt="Enter reference:",
                                            initialvalue=0)
        
        selections = self.collection_manager.get_selection()
        for coll_name, spec_name in selections:
            collection = self.collections[coll_name]
            if spec_name is None:
                collection.jump_correct(splices=splices,
                                        reference=reference)
            else:
                spectrum = collection.get_spectrum(spec_name).jump_correct(splices=splices,
                                                                           reference=reference)
        self.viewer.update()

    def groupby(self):
        separator = simpledialog.askstring(title="Group by",
                                           prompt="Enter separator:",
                                           initialvalue="_")
        if separator is None:
            return
        indices = simpledialog.askstring(title="Group by",
                               prompt="Enter indices (i.e. 0, 1, 2):")
        if indices is None:
            return
        indices = list(map(int, indices.replace(" ", "").split(","))) # convert to list
        selections = self.collection_manager.get_selection()
        groupby_collection = Collection(name="selection")
        for coll_name, spec_name in selections:
            if spec_name is None:
                # collection
                collection = self.collections[coll_name]
                for spectrum in collection.spectrums:
                    groupby_collection.add_spectrum(spectrum)
            else:
                # spectrum
                spectrum = self.collections[coll_name].get_spectrum(spec_name)
                groupby_collection.add_spectrum(spectrum)

        groups = groupby_collection.group_by(separator=separator,
                                             indices=indices)

        for group_id, group_coll in groups.items():
            self.add_collection(group_coll)
        
    
    def test_read(self):
        """ reads collections for testing """
        c = Collection("Test Collection")
        c.read("../../data/asd/")
        self.add_collection(c)
        c2 = Collection("Test Collection 2")
        c2.read("/home/younghoon/data/specdal/Big_Bio_2014/20140611/")
        c2.resample()
        c2.stitch()
        self.add_collection(c2)
        c3 = Collection("Test Collection 3")
        c3.read("/home/younghoon/data/specdal/SVC_LCRPPro_20150508/")
        self.add_collection(c3)

    def plot(self):
        """ TODO: plots selection for testing """
        selections = self.collection_manager.get_selection()
        plot_collection = Collection(name="Selection")
        for coll_name, spec_name in selections:
            if spec_name is None:
                # collection
                collection = self.collections[coll_name]
                for spectrum in collection.spectrums:
                    plot_collection.add_spectrum(spectrum)
            else:
                # spectrum
                spectrum = self.collections[coll_name].get_spectrum(spec_name)
                plot_collection.add_spectrum(spectrum)
        self.viewer.data = plot_collection
        self.viewer.update()

    def read_dir(self):
        # ask for directory
        directory = filedialog.askdirectory()
        if len(directory) == 0:
            return
        # ask for name
        name = "Test Collection" + str(len(self.collections))
        # ask for recursion
        recursive = False
        # ask for filetype
        c = Collection(name)
        c.read(directory, recursive=False)

        # add to manager
        self.add_collection(c)

    def read_files(self, files=[]):
        # ask for files
        files = filedialog.askopenfilenames()
        if len(files) == 0:
            return

        # ask for name
        coll_name = "Test Collection" + str(len(self.collections))
        if coll_name in self.collections:
            c = self.collections[coll_name]
        else:
            c = Collection(coll_name)
            self.add_collection(c)
        
        for f in files:
            spectrum = r.read(f)
            if spectrum is not None:
                c.add_spectrum(spectrum)

        self.collection_manager.update(coll_name)

    @property
    def collections(self):
        return self._collections

    @collections.setter
    def collections(self, value):
        self._collections = OrderedDict()

    def add_collection(self, collection):
        if isinstance(collection, Collection):
            self._collections[collection.name] = collection
            self.collection_manager.add_collection(collection)

        

def main():
    c = Collection("Test Collection")
    c.read("../../data/asd/")
    root = tk.Tk()
    session = Session(root)
    root.mainloop()


if __name__ == "__main__":
    main()