import argparse

import sys
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.abspath(".."))
from specdal import spectrum as s
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
sess = session.Session()

# read files
sess.read(directory=args.indir, recursive=args.recursive)

# resample
if args.resampler:
    sess.resample()

# stitch
if args.jump_correct:
    # parse command line args
    args.jump_correct = list(map(int, args.jump_correct))
    reference = args.jump_correct[0]
    splice = args.jump_correct[1:]
    
    # stitch the asd spectrum
    sess.jump_correct(waves=splice, reference=reference, fmt="asd")

# overlap stitch
if args.stitcher:
    sess.stitch(method=args.stitcher)

# group by
if args.group_by_separator:
    groups = sess.group_by_separator(*args.group_by_separator)

# save figures and csv
sess.save_figs(outdir=figdir)
sess.save_csv(outdir=datadir)

# save mask file
maskpath = os.path.join(outdir, 'mask.csv')
sess.mask.to_csv(maskpath)
