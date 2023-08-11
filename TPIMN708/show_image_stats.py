#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This is a description of the script. This description will appear in the help
when typing
>>> python view_image.py -h

To see the args received, a basic example can be:
>>> python view_image.py 'my_file.nii.gz' 1.0

The complete example can be:
>>> python view_image.py 'my_file.nii.gz' 1.0
        --optional_float 0.001 --optional_int 2
        --group_arg1 'Hello' --group_arg2 'You' --use_option_Y -v
"""

# First import basic python libraries
import argparse
import logging
from functions.data_processing.Michelson_Contrast import Michelson_Contrast
from functions.data_processing.RMS import RMS

# Then import yours.
# Encapsulate your methods in sub-files.
# Give them understandable names
# Import by alphabetical order for nicer view.
from functions.data_processing.compute_img_stats import voxel_and_image_size
from functions.utils.io import load_image
from functions.utils.manage_args import (
    verify_file_exists, verify_file_is_nifti)
from functions.img_viewer.img_viewer import viewer


def _build_arg_parser():
    p = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawTextHelpFormatter)

    p.add_argument('filename',
                   help="Image filename to be loaded. "
                        "file. ")  # Always write a good explanation!

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
    from_nifti=verify_file_is_nifti(args.filename)

    # logging_level = 'DEBUG' if args.verbose else 'INFO'
    # logging.basicConfig(level=logging_level)

    # 2. Load data
    logging.info("Loading data")
    img = load_image(args.filename, from_nifti)

    # 3. Process data
    # voxel_and_image_size(img)
    print('Michelson_Contrast: ', Michelson_Contrast(img, from_nifti))
    print('RMS: ', RMS(img, from_nifti))


if __name__ == "__main__":
    main()
