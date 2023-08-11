# -*- coding: utf-8 -*-

# Import basic python libraries
import logging
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, RangeSlider, Button
import numpy as np
# Import our tools
from functions.data_processing.compute_mip import mip_img, MIP_img


def viewer(img):
    """
    viewer verifies is either 3D or 4D and dispatches 3D images to viewer3d and 4D images to viewer4d

    Parameters
    ----------
    img:
        Nibabel image to be viewed for 3d or 4d images, numpy array for 2d images
    """
    img_shape = np.asarray(img.shape)
    print(img_shape)
    if len(img_shape) == 2:
        viewer2d(img)
        logging.info("2d data")
    elif len(img_shape) == 3:
        img_data = np.asarray(img.get_fdata())
        viewer3d(img_data, img_shape)
        logging.info("3d data")
    elif len(img_shape) == 4:
        img_data = np.asarray(img.get_fdata())
        viewer4d(img_data, img_shape)
        logging.info("4d data")
    else:
        logging.error("image is neither 2D, 3D or 4D")


def viewer2d(img_data):
    """
    viewer for 2D images. No information on slice position

    Parameters
    ----------
    img_data: numpy.ndarray
        image data information (all voxel intensities are encoded in a numpy array)
    """
    fig, ax = plt.subplots(1, 1)
    ax.imshow(img_data[:, :])
    ax.set_title("Slice of image")
    plt.show()

def viewer3d(img_data, img_shape):
    """
    viewer for 3D images. Code was inspired by https://matplotlib.org/stable/gallery/widgets/slider_demo.html

    Parameters
    ----------
    img_data: numpy.ndarray
        image data information (all voxel intensities are encoded in a numpy array)
    img_shape: numpy.ndarray
        image shape information (all dimension voxel lengths are encoded in a numpy array)
    """
    # Define initial position
    pos_init = img_shape // 2

    fig, ax = plt.subplots(1, 3)
    img_view_axial = ax[0].imshow(img_data[:, :, pos_init[2]].T, origin='lower')
    ax[0].set_title("Axial slice of image")
    ax[0].set_xlabel("left/right axis")
    ax[0].set_ylabel("posterior/anterior axis")
    ax[0].set_title("Axial slice of image")
    img_view_coronal = ax[1].imshow(img_data[:, pos_init[1], :].T, origin='lower')
    ax[1].set_xlabel("left/right axis")
    ax[1].set_ylabel("inferior/superior axis")
    ax[1].set_title("Coronal slice of image")
    img_view_sagital = ax[2].imshow(img_data[pos_init[0], :, :].T, origin='lower')
    ax[2].set_xlabel("posterior/anterior axis")
    ax[2].set_ylabel("inferior/superior axis")
    ax[2].set_title("Sagital slice of image")

    # adjust the main plot to make room for the sliders
    plt.subplots_adjust(bottom=0.5)

    # Make a inferior/superior slider to control the axial slice.
    axPos_axial = plt.axes([0.25, 0.1, 0.65, 0.03])
    pos_slider_axial = RangeSlider(
        ax=axPos_axial,
        label='Slice position [axial]',
        valmin=0,
        valmax=img_shape[2] - 1,
        valstep=1,
    )
    # Make a posterior/anterior slider to control the coronal slice.
    axPos_coronal = plt.axes([0.25, 0.2, 0.65, 0.03])
    pos_slider_coronal = RangeSlider(
        ax=axPos_coronal,
        label='Slice position [coronal]',
        valmin=0,
        valmax=img_shape[1] - 1,
        valstep=1,
    )
    # Make a left/right slider to control the sagittal slice.
    axPos_sagital = plt.axes([0.25, 0.3, 0.65, 0.03])
    pos_slider_sagital = RangeSlider(
        ax=axPos_sagital,
        label='Slice position [sagital]',
        valmin=0,
        valmax=img_shape[0] - 1,
        valstep=1,
    )
    # Create a `matplotlib.widgets.Button` to view mip projection.
    mip_button = plt.axes([0.15, 0.01, 0.3, 0.05])
    button_mip = Button(mip_button, 'View mip', hovercolor='0.975')
    # Create a `matplotlib.widgets.Button` to view MIP projection.
    MIP_button = plt.axes([0.55, 0.01, 0.3, 0.05])
    button_MIP = Button(MIP_button, 'View MIP', hovercolor='0.975')

    # The function to be called anytime the mip button is pressed
    def view_mip(event):
        """
        The function to be called anytime the mip button is pressed to compute mip projection

        Parameters
        ----------
        event:
            button press
        """
        range_axial = [int(pos_slider_axial.val[0]), int(pos_slider_axial.val[1])]
        range_coronal = [int(pos_slider_coronal.val[0]), int(pos_slider_coronal.val[1])]
        range_sagital = [int(pos_slider_sagital.val[0]), int(pos_slider_sagital.val[1])]
        mip_axial, mip_coronal, mip_sagital = mip_img(img_data, range_axial, range_coronal, range_sagital)
        img_view_axial.set_data(mip_axial.T)
        img_view_coronal.set_data(mip_coronal.T)
        img_view_sagital.set_data(mip_sagital.T)
        fig.canvas.draw_idle()

    # The function to be called anytime the MIP button is pressed
    def view_MIP(event):
        """
        The function to be called anytime the MIP button is pressed to compute MIP projection

        Parameters
        ----------
        event:
            button press
        """
        range_axial = [int(pos_slider_axial.val[0]), int(pos_slider_axial.val[1])]
        range_coronal = [int(pos_slider_coronal.val[0]), int(pos_slider_coronal.val[1])]
        range_sagital = [int(pos_slider_sagital.val[0]), int(pos_slider_sagital.val[1])]
        MIP_axial, MIP_coronal, MIP_sagital = MIP_img(img_data, range_axial, range_coronal, range_sagital)
        img_view_axial.set_data(MIP_axial.T)
        img_view_coronal.set_data(MIP_coronal.T)
        img_view_sagital.set_data(MIP_sagital.T)
        fig.canvas.draw_idle()

    # The function to be called anytime a slider's value changes
    def update(val):
        """
        The function to be called anytime a slider's value changes

        Parameters
        ----------
        val: list
            RangeSlider values. val[0]: start of range and val[1]: end of range
        """
        img_view_axial.set_data(img_data[:, :, int(pos_slider_axial.val[0])].T)
        img_view_coronal.set_data(img_data[:, int(pos_slider_coronal.val[0]), :].T)
        img_view_sagital.set_data(img_data[int(pos_slider_sagital.val[0]), :, :].T)
        fig.canvas.draw_idle()

    # register the update function with each slider
    button_mip.on_clicked(view_mip)
    button_MIP.on_clicked(view_MIP)
    pos_slider_axial.on_changed(update)
    pos_slider_coronal.on_changed(update)
    pos_slider_sagital.on_changed(update)
    plt.show()


def viewer4d(img_data, img_shape):
    """
    viewer for 4D images. Code was inspired by https://matplotlib.org/stable/gallery/widgets/slider_demo.html

    Parameters
    ----------
    img_data: numpy.ndarray
        image data information (all voxel intensities are encoded in a numpy array)
    img_shape: numpy.ndarray
        image shape information (all dimension voxel lengths are encoded in a numpy array)
    """
    # Define initial position of viewer
    pos_init = img_shape // 2

    # plot initial positions
    fig, ax = plt.subplots(1, 3)
    img_view_axial = ax[0].imshow(img_data[:, :, pos_init[2], pos_init[3]].T, origin='lower')
    ax[0].set_title("Axial slice of image")
    img_view_coronal = ax[1].imshow(img_data[:, pos_init[1], :, pos_init[3]].T, origin='lower')
    ax[1].set_title("Coronal slice of image")
    img_view_sagital = ax[2].imshow(img_data[pos_init[0], :, :, pos_init[3]].T, origin='lower')
    ax[2].set_title("Sagital slice of image")

    # adjust the main plot to make room for the sliders
    plt.subplots_adjust(bottom=0.5)

    # Make a inferior/superior slider to control the axial slice.
    axPos_axial = plt.axes([0.25, 0.1, 0.65, 0.03])
    pos_slider_axial = RangeSlider(
        ax=axPos_axial,
        label='Slice position [axial]',
        valmin=0,
        valmax=img_shape[2] - 1,
        valstep=1,
    )
    # Make a posterior/anterior slider to control the coronal slice.
    axPos_coronal = plt.axes([0.25, 0.2, 0.65, 0.03])
    pos_slider_coronal = RangeSlider(
        ax=axPos_coronal,
        label='Slice position [coronal]',
        valmin=0,
        valmax=img_shape[1] - 1,
        valstep=1,
    )
    # Make a left/right slider to control the sagittal slice.
    axPos_sagital = plt.axes([0.25, 0.3, 0.65, 0.03])
    pos_slider_sagital = RangeSlider(
        ax=axPos_sagital,
        label='Slice position [sagital]',
        valmin=0,
        valmax=img_shape[0] - 1,
        valstep=1,
    )
    # Make a 4th dimension slider to control the 4th dimension.
    axPos_4d = plt.axes([0.25, 0.4, 0.65, 0.03])
    pos_slider_4d = Slider(
        ax=axPos_4d,
        label='Slice position [4d]',
        valmin=0,
        valmax=img_shape[3] - 1,
        valinit=0,
        valstep=1,
    )

    # Create a `matplotlib.widgets.Button` to view mip projection.
    mip_button = plt.axes([0.15, 0.01, 0.3, 0.05])
    button_mip = Button(mip_button, 'View mip', hovercolor='0.975')
    # Create a `matplotlib.widgets.Button` to view MIP projection.
    MIP_button = plt.axes([0.55, 0.01, 0.3, 0.05])
    button_MIP = Button(MIP_button, 'View MIP', hovercolor='0.975')

    # The function to be called anytime the mip button is pressed
    def view_mip(event):
        """
        The function to be called anytime the mip button is pressed to compute mip projection

        Parameters
        ----------
        event:
            button press
        """
        range_axial = [int(pos_slider_axial.val[0]), int(pos_slider_axial.val[1])]
        range_coronal = [int(pos_slider_coronal.val[0]), int(pos_slider_coronal.val[1])]
        range_sagital = [int(pos_slider_sagital.val[0]), int(pos_slider_sagital.val[1])]
        val_4d = int(pos_slider_4d.val)
        mip_axial, mip_coronal, mip_sagital = mip_img(img_data, range_axial, range_coronal, range_sagital, val_4d)
        img_view_axial.set_data(mip_axial.T)
        img_view_coronal.set_data(mip_coronal.T)
        img_view_sagital.set_data(mip_sagital.T)
        fig.canvas.draw_idle()


    def view_MIP(event):
        """
        The function to be called anytime the MIP button is pressed to compute MIP projection

        Parameters
        ----------
        event:
            button press
        """
        range_axial = [int(pos_slider_axial.val[0]), int(pos_slider_axial.val[1])]
        range_coronal = [int(pos_slider_coronal.val[0]), int(pos_slider_coronal.val[1])]
        range_sagital = [int(pos_slider_sagital.val[0]), int(pos_slider_sagital.val[1])]
        val_4d = int(pos_slider_4d.val)
        MIP_axial, MIP_coronal, MIP_sagital = MIP_img(img_data, range_axial, range_coronal, range_sagital, val_4d)
        img_view_axial.set_data(MIP_axial.T)
        img_view_coronal.set_data(MIP_coronal.T)
        img_view_sagital.set_data(MIP_sagital.T)
        fig.canvas.draw_idle()

    def update(val):
        """
        The function to be called anytime a slider's value changes

        Parameters
        ----------
        val: list
            RangeSlider values. val[0]: start of range and val[1]: end of range
        """
        img_view_axial.set_data(img_data[:, :, int(pos_slider_axial.val[0]), int(pos_slider_4d.val)].T)
        img_view_coronal.set_data(img_data[:, int(pos_slider_coronal.val[0]), :, int(pos_slider_4d.val)].T)
        img_view_sagital.set_data(img_data[int(pos_slider_sagital.val[0]), :, :, int(pos_slider_4d.val)].T)
        fig.canvas.draw_idle()

    # register the update function with each slider
    button_mip.on_clicked(view_mip)
    button_MIP.on_clicked(view_MIP)
    pos_slider_4d.on_changed(update)
    pos_slider_axial.on_changed(update)
    pos_slider_coronal.on_changed(update)
    pos_slider_sagital.on_changed(update)
    plt.show()

