import argparse

import sys
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.abspath(".."))
from specdal import spectrum as s
from specdal import collection as c
from specdal import readers as r

# parse command line args
parser = argparse.ArgumentParser(description="SpecDAL Pipeline")

parser.add_argument('indir', help='input directory')
parser.add_argument('outdir', help='output directory')
parser.add_argument('-res', '--resampler', choices=['slinear', 'spline'],
                    default=None)
parser.add_argument('-sti', '--stitcher', choices=['mean', 'blending'],
                    default=None)
parser.add_argument('-gsep', '--group_by_separator', nargs='*',
                    default=None, help='First arg specifies the separator. Remaining args specify positions for forming a group',
                    metavar="separator")

args = parser.parse_args()

# make output directory
outdir = os.path.abspath(args.outdir)
figdir = os.path.join(outdir, 'figures')
datadir = os.path.join(outdir, 'data')
for d in (outdir, figdir, datadir):
    if not os.path.exists(d):
        os.makedirs(d)
    
################################################################################
# read files
coll = c.Collection()
for f in os.listdir(args.indir):
    filepath = os.path.join(args.indir, f)
    spec = r.read(filepath)
    coll.add_spectrum(spec)

# resample
if args.resampler:
    for spec in coll.spectra:
        spec.resample(method=args.resampler)

# stitch
if args.stitcher:
    for spec in coll.spectra:
        spec = sti.stitch(spec, method=args.stitcher)

# group by
if args.group_by_separator:
    groups = coll.group_by_separator(*args.group_by_separator)

# save figures and data
for gname, gdata in groups:
    ax = gdata.plot(title=gname)
    ax.set_ylabel('reflectance %')
    figpath = os.path.join(figdir, gname + '.png')
    datapath = os.path.join(datadir, gname + '.csv')
    plt.savefig(os.path.join(figpath), bbox_inches='tight')
    gdata.transpose().to_csv(datapath)

# save mask
maskpath = os.path.join(outdir, 'mask.csv')
coll.mask.to_csv(maskpath)

