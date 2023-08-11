# -*- coding: utf-8 -*-
import nibabel as nib
import numpy as np
import matplotlib.image as mpimg
from PIL import Image


def _load_nifti(filename):
    """
    load_nifti loads image from filename with nibabel and returns the loaded image as a nibabel image

    Parameters
    ----------
    filename: str
        Image filename to be loaded.

    Returns
    -------
    img: Nifti1Image
        The loaded image, as a nibabel image.
    """
    img = nib.load(filename)
    return img


def _load_png_jpg(filename):
    """
    load_png_jpg loads image from filename with matplotlib and returns the loaded image as a numpy array.

    Parameters
    ----------
    filename: str
        Image filename to be loaded.

    Returns
    -------
    img: np.ndarray
        The loaded image, as a numpy array.
    """
    image = Image.open(filename).convert('L')
    img = np.array(image).astype(float)
    return img


def load_image(filename, from_nifti=False):
    """
    load_image loads image from filename and returns the loaded image ad a numpy array

    Parameters
    ----------
    filename: str
        Image filename to be loaded.
    from_nifti: bool
        If this value is true, we will load the image from nibabel. Else,
        (default), we expect value to be loadable from matplotlib (ex, png,
        jpg).

    Returns
    -------
    img: np.ndarray
        The loaded image, as a numpy array if jpg/png or Nifti1Image if nifti format.
    """
    if from_nifti:
        return _load_nifti(filename)
    else:
        return _load_png_jpg(filename)
