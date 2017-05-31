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
if args.resampler:
    for spec in c.spectrums:
        spec.resample()
    
# overlap stitch
if args.stitcher:
    for spec in c.spectrums:
        spec.stitch(method=args.stitcher)

# stitch
if args.jump_correct:
    # parse command line args
    args.jump_correct = list(map(int, args.jump_correct))
    reference = args.jump_correct[0]
    splices = args.jump_correct[1:]
    
    # stitch the asd spectrum
    for spec in c.spectrums:
        spec.jump_correct(splices=splices, reference=reference)
    
# group by
if args.group_by_separator:
    group_colls = c.group_by(separator=args.group_by_separator[0],
                                indices=args.group_by_separator[1:])


means = Collection("group_means") # collection of group means
for k, v in group_colls.items():
    # save group plot
    v.data.plot()
    plt.savefig(os.path.join(figdir, v.name + ".png"),  bbox_inches='tight')
    plt.close()
    # save group csv
    v.data.transpose().to_csv(os.path.join(datadir, v.name + ".csv"))
    # add group mean to means collection
    means.add_spectrum(v.aggregate("mean"))

# plot of means
means.data.plot()
plt.savefig(os.path.join(figdir, means.name + ".png"),  bbox_inches='tight')
plt.close()
means.data.transpose().to_csv(os.path.join(datadir, means.name + ".csv"))

# save mask file
# maskpath = os.path.join(outdir, 'mask.csv')
# sess.mask.to_csv(maskpath)
