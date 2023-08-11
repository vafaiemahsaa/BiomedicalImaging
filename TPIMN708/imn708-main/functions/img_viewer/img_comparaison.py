# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt


def viewer_comparaison(img_original, img_transformed):
    """
    comparison viewer for 3D images pre and post denoising.

    Parameters
    ----------
    img_original: numpy.ndarray
        original image data information (all voxel intensities are encoded in a numpy array)
    img_transformed: numpy.ndarray
        denoised image data information (all dimension voxel lengths are encoded in a numpy array)
    """
    # find middle axial slice
    img_shape = img_original.shape
    middle_axial_slice = int(img_shape[2] // 2)
    # plot img comparaison
    fig, ax = plt.subplots(1, 2, sharey=True)
    ax[0].imshow(img_original[:, :, middle_axial_slice].T, origin='lower')
    ax[0].set_title("Original image")
    ax[0].set_xlabel("left/right axis")
    ax[0].set_ylabel("posterior/anterior axis")
    ax[1].imshow(img_transformed[:, :, middle_axial_slice].T, origin='lower')
    ax[1].set_title("Denoised image")
    ax[1].set_xlabel("left/right axis")
    fig.suptitle('middle axial slice before and after denoising')
    plt.show()


