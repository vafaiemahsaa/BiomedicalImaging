#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
view_image is automated script for image denoising and comparative plotting.

Command usage example
>>> python denoise_image.py 'my_file.nii.gz' --method 'gaussian' --sigma 2
"""

# Import basic python libraries
import argparse
import logging
import nibabel as nib
import os

# Import our tools
from functions.utils.io import load_image
from functions.utils.manage_args import (
    verify_file_exists, verify_file_is_nifti)
from functions.data_processing.filter_img import denoise_img


def _build_arg_parser():
    p = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawTextHelpFormatter)

    p.add_argument('filename',
                   help="Image filename to be loaded. Image should be a nifti "
                        "file.")
    p.add_argument('--method',
                   help="Denoising method. choices: 'gaussian', 'median', 'nl_means'")

    gaussian = p.add_argument_group(title='Options concerning gaussian filter')
    gaussian.add_argument('--sigma',
                          type=int,
                          default=1,
                          help="Standard deviation for Gaussian kernel. The standard deviations of the Gaussian "
                               "filter are given for each axis as a sequence, or as a single number, in which case "
                               "it is equal for all axes. Example --sigma 2")

    median = p.add_argument_group(title='Options concerning median filter')
    median.add_argument('--size',
                          type=int,
                          default=3,
                          help="size gives the shape that is taken from the input array, at every element position, "
                               "to define the input to the filter function. Example --size 5")

    nl_means = p.add_argument_group(title='Options concerning nl_means filter')
    nl_means.add_argument('--patch_size',
                          type=int,
                          default=7,
                          help="Size of patches used for denoising. Example: --patch_size 7 -> 7x7x7 patches")
    nl_means.add_argument('--patch_distance',
                          type=int,
                          default=11,
                          help="Maximal distance in pixels where to search patches used for denoising. "
                               "Example: --patch_distance 11 -> 23x23x23 search area")

    p.add_argument('--output',
                   action='store_true',
                   help="Use flag to save denoised image else the image is not saved. By default the image is saved "
                        "under the same filename as input with suffix '_<denoise methode>'")

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
    verify_file_is_nifti(args.filename)

    logging_level = 'DEBUG' if args.verbose else 'INFO'
    logging.basicConfig(level=logging_level)

    # 2. Load data
    logging.info("Loading data")
    img = load_image(args.filename, from_nifti=True)

    # 3. Process data
    denoised_image = denoise_img(img, args.method, args.sigma, args.size, args.patch_size, args.patch_distance)

    # 4. Save image
    if args.output:
        path, ext = os.path.splitext(args.filename)
        denoised_nib = nib.Nifti1Image(denoised_image, affine=img.affine, header=img.header)
        nib.save(denoised_nib, path + '_' + args.method + ext)


if __name__ == "__main__":
    main()
