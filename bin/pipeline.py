import argparse

import sys
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.abspath(".."))
from specdal.spectrum import Spectrum
from specdal.collection import Collection
from specdal import session
from specdal import readers as r

# parse command line args
parser = argparse.ArgumentParser(description="SpecDAL Pipeline")

parser.add_argument('indir', default=None, help='input directory')
parser.add_argument('outdir', default=None, help='output directory')
parser.add_argument('-res', '--resampler', choices=['slinear', 'spline'],
                    default=None)
parser.add_argument('-sti', '--stitcher', choices=['mean', 'blending'],
                    default=None)
parser.add_argument('-jump', '--jump_correct', nargs='*',
                    default=None, help="First arg specifies the reference. Remaining args specify the splice wavelengths. i.e. -jump 0 1000 1800")
parser.add_argument('-gsep', '--group_by_separator', nargs='*',
                    default=None, help='First arg specifies the separator. Remaining args specify positions for forming a group',
                    metavar="separator")
parser.add_argument('-gfunc', '--group-function', choices=['average', 'max', 'min'], nargs=1,
                    default=None, help='Function applied to each group [average | otherstocome]',
                    metavar="gfunction")
parser.add_argument('-r', '--recursive', action='store_true', default=False, help='recursively walk through input directory and process files')

args = parser.parse_args()

# make output directory
outdir = os.path.abspath(args.outdir)
figdir = os.path.join(outdir, 'figures')
datadir = os.path.join(outdir, 'data')
for d in (outdir, figdir, datadir):
    if not os.path.exists(d):
        os.makedirs(d)
    
################################################################################
# create session

# read directory into collection
c = Collection(name="original")
c.read(path=args.indir)

# resample
c.resample()

# overlap stitch
c.stitch()

# stitch
if args.jump_correct:
    # parse command line args
    args.jump_correct = list(map(int, args.jump_correct))
    reference = args.jump_correct[0]
    splices = args.jump_correct[1:]

    # stitch
    c.jump_correct(splices, reference=reference)
    
# group by
if args.group_by_separator:
    # get a dictionary containing group collections
    means = c.group_by(separator=args.group_by_separator[0],
                       aggr_fcn="mean",
                       indices=args.group_by_separator[1:])

for spec in means.spectrums:
    c.add_spectrum(spec)

group_colls = c.group_by(separator=args.group_by_separator[0],
                         indices=args.group_by_separator[1:])

for group_id, group_coll in group_colls.items():
    # save group plot
    group_coll.plot()
    plt.savefig(os.path.join(figdir, group_coll.name + ".png"),  bbox_inches='tight')
    plt.close()
    # save group csv
    group_coll.to_csv(os.path.join(datadir, group_coll.name + ".csv"))

# plot of means
means.plot()
plt.savefig(os.path.join(figdir, means.name + ".png"),  bbox_inches='tight')
plt.close()
means.to_csv(os.path.join(datadir, means.name + ".csv"))

# save mask file
maskpath = os.path.join(outdir, 'mask.csv')
c.masks.to_csv(maskpath)
