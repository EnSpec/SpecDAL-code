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

parser.add_argument('indir', default=None, help='input directory')
parser.add_argument('outdir', default=None, help='output directory')
parser.add_argument('-res', '--resampler', choices=['slinear', 'spline'],
                    default=None)
parser.add_argument('-sti', '--stitcher', choices=['mean', 'blending'],
                    default=None)
parser.add_argument('-jsti', '--jump_stitcher', nargs='*',
                    default=None, help="First arg specifies the reference. Remaining args specify the splice wavelengths. i.e. -jsti 0 1000 1800")
parser.add_argument('-gsep', '--group_by_separator', nargs='*',
                    default=None, help='First arg specifies the separator. Remaining args specify positions for forming a group',
                    metavar="separator")
parser.add_argument('-r', '--recursive', default=None, help='recursively walk through input directory and process files')

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
print("################################################################################")
print("READING...\n")
coll = c.Collection()
for f in os.listdir(args.indir):
    print("reading", f)
    filepath = os.path.join(args.indir, f)
    spec = r.read(filepath)
    coll.add_spectrum(spec)
print("reading: DONE")

# resample
if args.resampler:
    print("################################################################################")
    print("RESAMPLING...\n")
    for spec in coll.spectra:
        print("resampling", spec.name)
        spec.resample(method=args.resampler)
    print("resampling: DONE")

# jump correct
if args.jump_stitcher:
    print("################################################################################")
    print("JUMP CORRECTING...\n")
    args.jump_stitcher = list(map(int, args.jump_stitcher))
    reference = args.jump_stitcher[0]
    splice = args.jump_stitcher[1:]
    for spec in coll.spectra:
        # if asd: waves = spec.metadata['splice']
        spec.stitch(method='jump', waves=splice, reference=reference)
    print("jump correcting: DONE")

# stitch
if args.stitcher:
    print("################################################################################")
    print("STITCHING...\n")
    for spec in coll.spectra:
        spec = spec.stitch(method=args.stitcher)
    print("stitching: DONE")
        

# group by
if args.group_by_separator:
    print("################################################################################")
    print("GROUPING...\n")
    groups = coll.group_by_separator(*args.group_by_separator)
    print("grouping: DONE")

# save result
print("################################################################################")
print("SAVING...\n")
for gname, gdata in groups:
    figpath = os.path.join(figdir, gname + '.png')
    datapath = os.path.join(datadir, gname + '.csv')
    # create figure
    ax = gdata.plot(title=gname)
    ax.set_ylabel('reflectance %')
    plt.savefig(os.path.join(figpath), bbox_inches='tight')
    plt.close()
    # save data
    gdata.transpose().to_csv(datapath)

# mask
print("################################################################################")
print("SAVING MASK...\n")
# save mask
maskpath = os.path.join(outdir, 'mask.csv')
coll.mask.to_csv(maskpath)

