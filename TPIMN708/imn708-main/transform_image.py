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

# Then import yours.
# Encapsulate your methods in sub-files.
# Give them understandable names
# Import by alphabetical order for nicer view.
from functions.utils.io import load_image
from functions.utils.manage_args import verify_file_exists, verify_file_is_nifti
from functions.utils.image import assert_same_shape
from functions.data_processing.img_transformation import generate_3d_grid, trans_rigid



def _build_arg_parser():
    p = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawTextHelpFormatter)

    p.add_argument('-theta',
                   help="Image filename to be loaded. Image should be a nifti "
                        "file.")  # Always write a good explanation!
    p.add_argument('-omega',
                   help="Image filename to be loaded. Image should be a nifti "
                        "file.")  # Always write a good explanation!
    p.add_argument('-phi',
                   help="Image filename to be loaded. Image should be a nifti "
                        "file.")  # Always write a good explanation!
    p.add_argument('-p',
                   help="Image filename to be loaded. Image should be a nifti "
                        "file.")  # Always write a good explanation!
    p.add_argument('-q',
                   help="Image filename to be loaded. Image should be a nifti "
                        "file.")  # Always write a good explanation!
    p.add_argument('-r',
                   help="Image filename to be loaded. Image should be a nifti "
                        "file.")  # Always write a good explanation!

    # Typical arg: add debugging prints or not
    p.add_argument('-v', action='store_true', dest='verbose',
                   help='If set, produces verbose output.')

    return p


def main():
    parser = _build_arg_parser()
    args = parser.parse_args()
    print("****\n"
          "Args that were received in the main method: \n{}\n"
          "****".format(args))

    # 1. Verifications
    logging_level = 'DEBUG' if args.verbose else 'INFO'
    logging.basicConfig(level=logging_level)

    # 2. Load data

    # 3. Process data
    #generate_3d_grid()
    trans_rigid()
    #trans_rigide(theta, omega, phi, p, q, r)


if __name__ == "__main__":
    main()
