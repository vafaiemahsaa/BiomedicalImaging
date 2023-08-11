# -*- coding: utf-8 -*-
import logging


def voxel_and_image_size(img):
    """
    blabla
    method: str
        Should be either 'method1' or 'method2'
    """
    # Prepare image for the denoising
    voxel_size = img.header['pixdim']
    print(voxel_size)
    img_size = img.header.get_data_shape()
    print(img_size)


def use_img_to_create_something(img, use_method_y):
    """
    blabla
    use_method_y: bool
        If true, use method y. Else, use method x.
    """
    if use_method_y:
        logging.debug("Using method Y!")
        result = 1
    else:
        logging.debug("NOT using method Y!")
        result = 5

    return result
