# -*- coding: utf-8 -*-
import logging

from scipy import ndimage
from scipy.ndimage import gaussian_filter, median_filter
from skimage.restoration import denoise_nl_means, estimate_sigma
import numpy as np
from functions.img_viewer.img_comparaison import viewer_comparaison


def denoise_img(img, method, sigma, size, patch_size, patch_distance):
    """
    Dispatches image to denoising method based on 'method'

    Parameters
    ----------
    img: nibabel Nifti1Image
        Nibabel image to be denoised
    method: str
        string contain denoising method

    Returns
    -------
    img_denoised: np.ndarray
        denoised image data information (all voxel intensities are encoded in a numpy array)
    """
    # Get image data
    img_data = np.asarray(img.get_fdata())

    # Actually do the denoising
    if method == 'nl_means':
        logging.debug("Using nl means filter!")
        img_denoised = nl_means_filter(img_data, patch_size, patch_distance)
        viewer_comparaison(img_data, img_denoised)
    elif method == 'gaussian':
        logging.debug("Using gaussian filter!")
        img_denoised = gaussian_filter(img_data, sigma)
        viewer_comparaison(img_data, img_denoised)
    elif method == 'median':
        logging.debug("Using median filter!")
        img_denoised = median_filter(img_data, size)
        viewer_comparaison(img_data, img_denoised)
    else:
        raise ValueError("Chosen method not understood.")

    return img_denoised


def nl_means_filter(img, patch_size, patch_distance):
    """
    Denoise image with nl_means filter

    Parameters
    ----------
    img: np.ndarray
        image data information (all voxel intensities are encoded in a numpy array)
    patch_size: int
        Size of patches used for denoising. Example: --patch_size 7 -> 7x7x7 patches
    patch_distance: int
        Maximal distance in pixels where to search patches used for denoising. Example: --patch_distance 11 -> 23x23x23
        search area

    Returns
    -------
    img_denoised: np.ndarray
        denoised image data information (all voxel intensities are encoded in a numpy array)
    """
    # estimate the noise standard deviation from the noisy image
    sigma_est = np.mean(estimate_sigma(img, channel_axis=-1))
    print(f'estimated noise standard deviation = {sigma_est}')

    patch_kw = dict(patch_size=patch_size,  # 7x7x7 patches
                    patch_distance=patch_distance,  # 23x23x23 search area
                    channel_axis=-1)

    logging.debug("Using nl_means not with fast method!")
    # slow algorithm
    img_denoised = denoise_nl_means(img, h=1 * sigma_est, fast_mode=False, **patch_kw)
    return img_denoised


def median_filter(img, size):
    """
    Denoise image with median filter

    Parameters
    ----------
    img: np.ndarray
        image data information (all voxel intensities are encoded in a numpy array)
    size: int
        size gives the shape that is taken from the input array, at every element position,
        to define the input to the filter function. Example --size 5

    Returns
    -------
    img_denoised: np.ndarray
        denoised image data information (all voxel intensities are encoded in a numpy array)
    """
    logging.debug("Using median filter!")
    img_denoised = ndimage.median_filter(img, size=size)
    return img_denoised

def gaussian_filter(img, sigma):
    """
    Denoise image with gaussian filter

    Parameters
    ----------
    img: np.ndarray
        image data information (all voxel intensities are encoded in a numpy array)
    sigma: int
        Standard deviation for Gaussian kernel. The standard deviations of the Gaussian filter are given for each
        axis as a sequence, or as a single number, in which case it is equal for all axes. Example --sigma 2

    Returns
    -------
    img_denoised: np.ndarray
        Denoised image data information (all voxel intensities are encoded in a numpy array)
    """

    logging.debug("Using gradient magnitude!")
    img_denoised = ndimage.gaussian_filter(img, sigma=sigma)
    return img_denoised


















