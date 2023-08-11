# -*- coding: utf-8 -*-
import logging
import os


def verify_file_exists(filename):
    """
    Assert that file exists else returns error

    Parameters
    ----------
    filename: str
        Image filename to verify existence.

    """
    if os.path.isfile(filename):
        file_was_found = True
    if not file_was_found:
        raise ValueError("Can't process this file, it was not found! \n{}"
                         .format(filename))


def verify_file_is_nifti(filename):
    """
    Assert that file is in nifti format else returns error

    Parameters
    ----------
    filename: str
        Image filename to verify nifti format.

    Return
    ----------
    from_nifti: bool
        True if image is in nifti format otherwise false

    """

    # Nifti = .nii or .nii.gz
    _, ext = os.path.splitext(filename)
    from_nifti = True

    if ext not in ['.nii', '.gz']:
        logging.warning("Expected nifti file, but extension was not .nii or "
                        ".nii.gz. Continuing with matplotlib loading!")
        from_nifti = False
    return from_nifti