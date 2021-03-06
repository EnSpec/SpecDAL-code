
# Table of Contents

1.  [Introduction](#org3d52f24)
2.  [Installation](#org2b3c105)
    1.  [Prerequisite](#org87bde83)
    2.  [Installing SpecDAL](#org0ea568a)
    3.  [Development version](#orgef8bdb2)
3.  [Features](#org94f8671)
    1.  [Example usage (TODO)](#org91f90c3)



<a id="org3d52f24"></a>

# Introduction

`SpecDAL` is a Python package for loading and manipulating field
spectroscopy data. It currently supports readers for ASD, SVC, and PSR
spectremeters. `SpecDAL` provides useful functions for processing and
aggregating the data. 


<a id="org2b3c105"></a>

# Installation

Currently, `SpecDAL` can be installed from Github. We plan to make it
available via Python's `pip` installer in the future.


<a id="org87bde83"></a>

## Prerequisite

1.  Install Python 3
    -   packages: pandas, numpy, matplotlib, etc.
2.  Install Git
3.  (Windows only) Install [Git-bash](https://git-for-windows.github.io/).


<a id="org0ea568a"></a>

## Installing SpecDAL

1.  Open terminal or Git-bash and navigate to the desired directory
    using `cd <directory>`.
2.  The following command will create a directory `SpecDAL-code`
    containing `SpecDAL`:
    
        git clone https://github.com/EnSpec/SpecDAL-code.git
3.  To update the package, go to `SpecDAL-code` directory and run the
    following command:
    
        git pull origin master


<a id="orgef8bdb2"></a>

## Development version

Development version is maintained in `dev` branch and production
version in `master`. For the latest development version, run the
following code:

    git fetch origin
    git branch dev


<a id="org94f8671"></a>

# Features

At its core, `SpecDAL` package provides python functions and data
structures to manipulate spectroscopy data in [specdal](./specdal/). Python users
can import the modules directly to write their own scripts.

We also provide interface via command-line pipeline and GUI in
[bin](./bin). 


<a id="org91f90c3"></a>

## Example usage (TODO)

