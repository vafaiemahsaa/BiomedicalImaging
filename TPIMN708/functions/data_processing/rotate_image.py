import numpy as np
from matplotlib import pyplot as plt
# from skimage import io

from scipy import ndimage


def rotate_image_nn(I, theta):

    I_R = np.zeros(I.shape, dtype=np.uint32)

    T = np.array([[np.cos(theta), np.sin(theta)], [-np.sin(theta), np.cos(theta)]])

    for i, row in enumerate(I):
        for j, col in enumerate(row):
            pixel_data = I[i, j]  # get the value of pixel at corresponding location
            input_coord = np.array([i, j])  # this will be my [x,y] matrix
            result = T @ input_coord
            i_r, j_r = result  # store the resulting coordinate location

            # make sure the i and j values remain within the index range
            if (0 < int(i_r) < I.shape[0]) and (0 < int(j_r) < I.shape[1]):
                I_R[int(i_r)][int(j_r)] = pixel_data

    # plt.imshow(I_R)
    # plt.show()
    return I_R

def rotate_image(I, theta_d):
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
    xv_t = T[0, 0] * xv + T[0, 1] * yv
    yv_t = T[1, 0] * xv + T[1, 1] * yv
    coord = [xv_t, yv_t]

    img_r = ndimage.map_coordinates(I, coord, order=5).T
    #ax[1].imshow(img_r)
    #ax[1].set_title("image with rotation theta: {}".format(round(theta_d,2)))
    #plt.show()
    return img_r
