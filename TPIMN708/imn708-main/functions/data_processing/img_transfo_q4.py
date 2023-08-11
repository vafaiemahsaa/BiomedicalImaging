# -*- coding: utf-8 -*-
import logging
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from mpl_toolkits import mplot3d
from PIL import Image
from scipy import interpolate


def main():
    """
    blabla
    method: str
        Should be either 'method1' or 'method2'
    """
    fig, ax = plt.subplots(1, 2, figsize=(10, 5))
    image = Image.open("/home/pabaua/Documents/UdeS/2022-Aut_IMN-708/TP/data/Data_TP2/TP2-Data_png/BrainMRI_1.jpg").convert('L')
    img = np.array(image)
    ax[0].imshow(img)
    x = np.arange(0, img.shape[0])
    y = np.arange(0, img.shape[1])
    f = interpolate.interp2d(x, y, img, kind='cubic')
    # image with translation
    x_new = np.arange(0, img.shape[0]) + 60
    y_new = np.arange(0, img.shape[1]) + 60
    ax[1].imshow(f(x_new, y_new))
    plt.show()


if __name__ == "__main__":
    main()





