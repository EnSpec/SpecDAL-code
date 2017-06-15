
# Table of Contents

1.  [Introduction](#org1d02f35)
2.  [Installation](#orge5c139a)
    1.  [Prerequisite](#org792f7ed)
    2.  [Installing SpecDAL](#org51cac1f)
    3.  [Development version](#orgfe486fb)
3.  [Features](#orgd65317d)
    1.  [Example usage (TODO)](#org7a71c92)



<a id="org1d02f35"></a>

# Introduction

`SpecDAL` is a Python package for loading and manipulating field
spectroscopy data. It currently supports readers for ASD, SVC, and PSR
spectremeters. `SpecDAL` provides useful functions for processing and
aggregating the data. 


<a id="orge5c139a"></a>

# Installation

Currently, `SpecDAL` can be installed from Github. We plan to make it
available via Python's `pip` installer in the future.


<a id="org792f7ed"></a>

## Prerequisite

1.  Install Python 3
    -   packages: pandas, numpy, matplotlib, etc.
2.  Install Git
3.  (Windows only) Install [Git-bash](https://git-for-windows.github.io/).


<a id="org51cac1f"></a>

## Installing SpecDAL

1.  Open terminal or Git-bash and navigate to the desired directory
    using `cd <directory>`.
2.  The following command will create a directory `SpecDAL-code`
    containing `SpecDAL`:
    
        git clone https://github.com/EnSpec/SpecDAL-code.git
3.  To update the package, go to `SpecDAL-code` directory and run the
    following command:
    
        git pull origin master


<a id="orgfe486fb"></a>

## Development version

Development version is maintained in `dev` branch and production
version in `master`. For the latest development version, run the
following code:

    git fetch origin
    git branch dev


<a id="orgd65317d"></a>

# Features

At its core, `SpecDAL` package provides python functions and data
structures to manipulate spectroscopy data in <./specdal/>. Python users
can import the modules directly to write their own scripts.

We also provide interface via command-line pipeline and GUI in
<./bin>. 


<a id="org7a71c92"></a>

## Example usage (TODO)

