# -*- coding: utf-8 -*-
import logging
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from sklearn.metrics import mutual_info_score


def ssd(img_I, img_J):
    """
    blabla
    method: str
        Should be either 'method1' or 'method2'
    """
    ssd_metric = np.sum((img_I-img_J)**2)
    print("The SSD is: {}".format(ssd_metric))

def cr(img_I, img_J):
    """
    blabla
    method: str
        Should be either 'method1' or 'method2'
    """
    cr_metric = np.corrcoef(img_I.ravel(), img_J.ravel())
    print("The CR is: {}".format(cr_metric))


def cr(img_I, img_J):
    """
    blabla
    method: str
        Should be either 'method1' or 'method2'
    """
    cr_metric = np.corrcoef(img_I.ravel(), img_J.ravel())[0][1]
    print("The CR is: {}".format(cr_metric))


def IM(img_I, img_J, bin):
    """
    blabla
    method: str
        Should be either 'method1' or 'method2'
    """
    img_I_data = img_I.astype(float)
    img_J_data = img_J.astype(float)
    #nb_pixels = img_I.shape[0]*img_I.shape[1]
    hist_2d = np.histogram2d(img_I_data.ravel(), img_J_data.ravel(), bins=bin)[0]
    MI_metric = mutual_info_score(None, None, contingency=hist_2d)
    print("The IM is: {}".format(MI_metric))


def plot_hist2d(hist_2d, xedges, yedges, img_I, img_J):
    fig, ax = plt.subplots(1,3, figsize=(17,5))
    i = ax[0].imshow(img_I)
    ax[0].set_title("image I")
    ax[0].set_xlabel("position x")
    ax[0].set_ylabel("position y")
    j = ax[1].imshow(img_J)
    ax[1].set_title("image J")
    ax[1].set_xlabel("position x")
    ax[1].set_ylabel("position y")
    hist = ax[2].imshow(hist_2d, interpolation='nearest', origin='lower', extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]], norm=colors.LogNorm())
    ax[2].set_title("joint histogram")
    ax[2].set_xlabel("image I intensity")
    ax[2].set_ylabel("image J intensity")
    plt.colorbar(i, ax=ax[0], shrink=0.8)
    plt.colorbar(j, ax=ax[1], shrink=0.8)
    plt.colorbar(hist, ax=ax[2], shrink=0.8)
    plt.show()


def assert_sum(hist_2d, img):
    print(img.shape[0]*img.shape[1])
    if np.sum(hist_2d) == img.shape[0]*img.shape[0]:
        print("Histogram is of right shape!")
    else:
        print("Histogram is not of right shape.")




