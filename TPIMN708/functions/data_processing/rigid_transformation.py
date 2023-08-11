import numpy as np
from matplotlib import pyplot as plt
# from skimage import io

from scipy import ndimage


def rigid_transformation(I, theta_d, p , q):
    theta = np.deg2rad(theta_d)
    T = np.array([[np.cos(theta), np.sin(theta)], [-np.sin(theta), np.cos(theta)]])
    #fig, ax = plt.subplots(1, 2, figsize=(10, 5))
    #ax[0].imshow(I)
    #ax[0].set_title("Original image")
    # original grid
    x = np.arange(0, I.shape[0])
    y = np.arange(0, I.shape[1])
    xv, yv = np.meshgrid(x, y)
    # grid with rotation
    xv_t = T[0, 0] * xv + T[0, 1] * yv - p
    yv_t = T[1, 0] * xv + T[1, 1] * yv - q
    coord = [xv_t, yv_t]

    img_r = ndimage.map_coordinates(I, coord, order=5).T
    #ax[1].imshow(img_r)
    #ax[1].set_title("image with rotation theta: {}, p: {}, q: {}".format(round(theta_d,2), p, q))
    #plt.show()
    return img_r
