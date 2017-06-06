import os
import sys
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
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
        tk.Button(self.mw, text="read", command = lambda : self.test_read()).grid(row=2, column=0)
        tk.Button(self.mw, text="plot", command = lambda : self.test_plot()).grid(row=2, column=1)

    def test_read(self):
        """ reads collections for testing """
        c = Collection("Test Collection")
        c.read("../../data/asd/")
        self.add_collection(c)
        # c2 = Collection("Test Collection 2")
        # c2.read("../../data/sig/")
        # c2.resample()
        # c2.stitch()
        # self.add_collection(c2)

    def test_plot(self):
        """ TODO: plots selection for testing """
        pass

    def read_dir(self, directory, recursive=False):
        pass

    def read_files(self, files=[]):
        pass

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
