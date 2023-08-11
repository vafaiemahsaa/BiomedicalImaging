import numpy as np
from matplotlib import pyplot as plt
from scipy import interpolate
from scipy import ndimage


def translate_image_nn(I, p, q):
    # x_size, y_size = I.shape[:]
    # T = np.array([[1, 0, p], [0, 1, q],[0,0,1]])
    I = np.float32(I)
    I_T = np.zeros(I.shape)
    # Interpolation by rounding p and q
    p = round(p)
    q = round(q)
    I_T[q:, p:] = I[:-q, :-p]
    # plt.imshow(I_T)
    # plt.show()

def translate_image_p(I, p, q):
    #fig, ax = plt.subplots(1, 2, figsize=(10, 5))
    #ax[0].imshow(I)
    x = np.arange(0, I.shape[0])
    y = np.arange(0, I.shape[1])
    f = interpolate.interp2d(x, y, I, kind='quintic')
    # coord with translation
    x_new = np.arange(0, I.shape[0]) - p
    y_new = np.arange(0, I.shape[1]) - q
    #ax[1].imshow(f(x_new, y_new))
    #plt.show()
    I_t = f(x_new, y_new)
    return I_t

def translate_image(I, p, q):
    #fig, ax = plt.subplots(1, 2, figsize=(10, 5))
    #ax[0].imshow(I)
    x = np.arange(0, I.shape[0]) - p
    y = np.arange(0, I.shape[1]) - q
    xv, yv = np.meshgrid(x, y)
    coord = [xv, yv]
    img_t = ndimage.map_coordinates(I, coord, order=5).T
    #ax[1].imshow(img_t)
    #plt.show()
    return img_t
