import os
import sys
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib
sys.path.insert(0, os.path.abspath("../.."))
from specdal.spectrum import Spectrum
from specdal.collection import Collection
from specdal import readers as r
matplotlib.use('TkAgg')


class Viewer(tk.Frame):
    def __init__(self, parent, data=None):
        tk.Frame.__init__(self, parent)
        self.fig = plt.Figure(figsize=(6,6))
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        NavigationToolbar2TkAgg(self.canvas, self) # for matplotlib features
        self.canvas.get_tk_widget().pack(side=tk.LEFT)
        self.data = data

        self.pack()

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        if isinstance(value, Collection) or isinstance(value, Spectrum):
            self._data = value
            self.update()
        else:
            self._data = None

    def update(self):
        """ Update the plot """
        print("updating plot")
        self.ax.clear()
        self.data.plot(ax=self.ax)
        self.ax.legend().remove()
        self.canvas.draw()


def main():
    c = Collection("Test Collection")
    c.read("../../data/asd/")
    root = tk.Tk()
    Viewer(root, c)
    root.mainloop()


if __name__ == "__main__":
    main()
