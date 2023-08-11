# -*- coding: utf-8 -*-
import logging
import os


def assert_same_shape(images):
    """
    Check the shape of multiple images.
    Parameters
    ----------
    images : array of string or string
        List of images or an image.
    """
    if isinstance(images, str):
        images = [images]

    if len(images) == 0:
        raise Exception("Can't check if images are of the same "
                        "shape. No image was given")

    for curr_image in images[1:]:
        if not condition_shape(images[0], curr_image):
            raise Exception("Images are not of the same shape")
        else:
            print("images are of same shape!")



def condition_shape(img_I, img_J):
    """
    Check the shape of 2 images.
    Parameters
    ----------
    images : array of string or string
        List of images or an image.
    """
    print("image I shape: {}".format(img_I.shape))
    print("image J shape: {}".format(img_J.shape))
    same_shape = True if img_I.shape == img_J.shape else False
    return same_shape
