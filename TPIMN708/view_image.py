#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
view_image is an interactive visualizer which
is used to display all slices in each plane and compute mip/MIP projections on main
plains: Axial, Coronal and Sagital

Command usage example
>>> python view_image.py 'my_file.nii.gz'
"""

# Import basic python libraries
import argparse
import logging

# Import our tools
from functions.utils.io import load_image
from functions.utils.manage_args import (
    verify_file_exists, verify_file_is_nifti)
from functions.img_viewer.img_viewer import viewer


def _build_arg_parser():
    p = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawTextHelpFormatter)

    p.add_argument('filename',
                   help="Image filename to be loaded. Image should be a nifti "
                        "file.")

    # Typical arg: add debugging prints or not
    p.add_argument('-v', action='store_true', dest='verbose',
                   help='If set, produces verbose output.')

    return p


def main():
    parser = _build_arg_parser()
    args = parser.parse_args()
    print("****\n"
          "Args that were received in the main method: {}\n"
          "****".format(args))

    # 1. Verifications
    verify_file_exists(args.filename)
    from_nifti = verify_file_is_nifti(args.filename)

    logging_level = 'DEBUG' if args.verbose else 'INFO'
    logging.basicConfig(level=logging_level)

    # 2. Load data
    logging.info("Loading data")
    img = load_image(args.filename, from_nifti)

    # 3. Process data
    viewer(img)


if __name__ == "__main__":
    main()
