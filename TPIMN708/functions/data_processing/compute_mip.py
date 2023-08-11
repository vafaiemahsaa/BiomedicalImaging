# -*- coding: utf-8 -*-

# Import basic python libraries
import numpy as np
import matplotlib.pyplot as plt


def mip_img(img_data, range_axial, range_coronal, range_sagital, val_4d=None):
    """
    Compute minimum intensity projection for each axis

    Parameters
    ----------
    img_data: numpy.ndarray
        image data information (all voxel intensities are encoded in a numpy array)
    range_axial: list
        inferior/superior axis range to compute mip. range_axial[0] -> start, range_axial[1] -> end
    range_coronal: list
        posterior/anterior axis range to compute mip. range_axial[0] -> start, range_axial[1] -> end
    range_sagital: list
        left/right axis range to compute mip. range_axial[0] -> start, range_axial[1] -> end
    val_4d: bool
        Take into account 4th dimension if True

    Returns
    -------
    mip_axial: np.ndarray
        mip projection on axial plane
    mip_coronal: np.ndarray
        mip projection on coronal plane
    mip_sagittal: np.ndarray
        mip projection on sagittal plane
    """
    # Verify image dimensions
    img_shape = img_data.shape
    if len(img_shape) == 3:
        mip_axial = np.amin(img_data[:, :, range_axial[0]:range_axial[1]], axis=2)
        mip_coronal = np.amin(img_data[:, range_coronal[0]:range_coronal[1], :], axis=1)
        mip_sagittal = np.amin(img_data[range_sagital[0]:range_sagital[1], :, :], axis=0)
    elif len(img_shape) == 4:
        mip_axial = np.amin(img_data[:, :, range_axial[0]:range_axial[1], val_4d], axis=2)
        mip_coronal = np.amin(img_data[:, range_coronal[0]:range_coronal[1], :, val_4d], axis=1)
        mip_sagittal = np.amin(img_data[range_sagital[0]:range_sagital[1], :, :, val_4d], axis=0)
    return mip_axial, mip_coronal, mip_sagittal

def MIP_img(img_data, range_axial, range_coronal, range_sagital, val_4d=None):
    """
    Compute maximum intensity projection for each axis

    Parameters
    ----------
    img_data: numpy.ndarray
        image data information (all voxel intensities are encoded in a numpy array)
    range_axial: list
        inferior/superior axis range to compute MIP. range_axial[0] -> start, range_axial[1] -> end
    range_coronal: list
        posterior/anterior axis range to compute MIP. range_axial[0] -> start, range_axial[1] -> end
    range_sagital: list
        left/right axis range to compute MIP. range_axial[0] -> start, range_axial[1] -> end
    val_4d: bool
        Take into account 4th dimension if True

    Returns
    -------
    MIP_axial: np.ndarray
        mip projection on axial plane
    MIP_coronal: np.ndarray
        mip projection on coronal plane
    MIP_sagittal: np.ndarray
        mip projection on sagittal plane
    """
    img_shape = img_data.shape
    if len(img_shape) == 3:
        MIP_axial = np.amax(img_data[:,:,range_axial[0]:range_axial[1]], axis=2)
        MIP_coronal = np.amax(img_data[:,range_coronal[0]:range_coronal[1],:], axis=1)
        MIP_sagittal = np.amax(img_data[range_sagital[0]:range_sagital[1],:,:], axis=0)
    elif len(img_shape) == 4:
        MIP_axial = np.amax(img_data[:,:,range_axial[0]:range_axial[1], val_4d], axis=2)
        MIP_coronal = np.amax(img_data[:,range_coronal[0]:range_coronal[1],:, val_4d], axis=1)
        MIP_sagittal = np.amax(img_data[range_sagital[0]:range_sagital[1],:,:, val_4d], axis=0)
    return MIP_axial, MIP_coronal, MIP_sagittal



def mip_MIP_viewr(img_data):
    """
    Plot Maximal and minimum intensity projection for each plane: axial, coronal, sagital

    Parameters
    ----------
    img_data: numpy.ndarray
        image data information (all voxel intensities are encoded in a numpy array)
    """
    mip_axial = np.amin(img_data, axis=2)
    mip_coronal = np.amin(img_data, axis=1)
    mip_sagital = np.amin(img_data, axis=0)
    MIP_axial = np.amax(img_data, axis=2)
    MIP_coronal = np.amax(img_data, axis=1)
    MIP_sagital = np.amax(img_data, axis=0)

    fig, ax = plt.subplots(2, 3)
    ax[0, 0].imshow(mip_axial.T, origin='lower')
    ax[0, 0].set_title("axial mip")
    ax[0, 1].imshow(mip_coronal.T, origin='lower')
    ax[0, 1].set_title("coronal mip")
    ax[0, 2].imshow(mip_sagital.T, origin='lower')
    ax[0, 2].set_title("sagital mip")
    ax[1, 0].imshow(MIP_axial.T, origin='lower')
    ax[1, 0].set_title("axial MIP")
    ax[1, 1].imshow(MIP_coronal.T, origin='lower')
    ax[1, 1].set_title("coronal MIP")
    ax[1, 2].imshow(MIP_sagital.T, origin='lower')
    ax[1, 2].set_title("sagital MIP")
    plt.show()
