from asyncio import sleep

import matplotlib
import numpy as np
from scipy.optimize import fmin_powell
import time
#from IPython import display

from matplotlib import pyplot as plt

# import cv2
#import IPython as ip
#from IPython.display import display, clear_output

from functions.data_processing.translate_image import translate_image



def SSD(I, J):
    """Computing the sum of squared differences (SSD) between two images."""
    if I.shape != J.shape:
        print("Images don't have the same shape.")
        return
    return np.sum((np.array(I, dtype=np.float32) - np.array(J, dtype=np.float32)) ** 2)


#         plt.plot(translation_y, ssd_y[1:])


def register_translation_ssd_m(I, J):
    ssd = []
    translation_x = []
    translation_y = []
    size_x = I.shape[1]  # width
    size_y = I.shape[0]
    translation_range_x = range(1, size_x)
    translation_range_y = range(1, size_y)
    for p in translation_range_x:
        for q in translation_range_y:
            I_T = translate_image(I, p, q)
            ssd.append(SSD(I_T, J))
            translation_x.append(p)
            translation_y.append(q)

    Q = translation_y[ssd.index(min(ssd))]
    P = translation_x[ssd.index(min(ssd))]
    ax = plt.axes(projection='3d')
    ax.plot3D(translation_x, translation_y, ssd, 'gray')
    plt.show()
    return translate_image(I, P, Q)


def register_translation_ssd(I, J, epsilon=10**(-8)):
    p, q = 0, 0
    I_p_q = translate_image(I, p, q)
    print_image(I, I_p_q, J)
    ssd_v = []
    for n in range(2000):
        #print_image(I, I_p_q, J)
        dSSD_dp = 2 * sum(sum((I_p_q - J) * np.gradient(I_p_q, axis=0)))
        dSSD_dq = 2 * sum(sum((I_p_q - J) * np.gradient(I_p_q, axis=1)))
        print(dSSD_dp)
        p = p + epsilon * dSSD_dp
        q = q + epsilon * dSSD_dq
        I_p_q = translate_image(I, p, q)
        print("SSD: {}, change in x: {} and in y: {}".format(SSD(I_p_q, J), p, q))
        ssd_v.append(SSD(I_p_q, J))
    print_image(I, I_p_q, J)
    plt.plot(ssd_v)
    plt.title("SSD in function of iteration")
    plt.ylabel("SSD")
    plt.xlabel("iteration")
    plt.show()

def print_image(I, I_p_q, J):
    fig, ax = plt.subplots(1, 3, figsize=(15, 5))
    ax[0].imshow(I)
    ax[0].set_title("Original image")
    ax[1].imshow(I_p_q)
    ax[1].set_title("Registered image")
    ax[2].imshow(J)
    ax[2].set_title("Destination image")
    plt.show()

