# -*- coding: utf-8 -*-
import logging
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from mpl_toolkits import mplot3d


def trans_rigid():
    xv, yv, zv = generate_3d_grid()
    transformation = transfo(xv, yv, zv, theta=0, omega=0, phi=0, p=0, q=0, r=0)
    transformation_m1 = np.matrix(
        [[0.9045, -0.3847, -0.1840, 10.0000], [0.2939, 0.8750, -0.3847, 10.0000], [0.3090, 0.2939, 0.9045, 10.0000],
         [0, 0, 0, 1.0000]])
    transformation_m2 = np.matrix(
        [[-0.0000, -0.2598, 0.1500, -3.0000], [0.0000, -0.1500, -0.2598, 1.5000], [0.3000, 0, 0, 0],
         [0, 0, 0, 1.0000]])
    transformation_m3 = np.matrix(
        [[0.7182, -1.3727, -0.5660, 1.8115], [-1.9236, -4.6556, -2.5512, 0.2873], [-0.6426, -1.7985, -1.6285, 0.7404],
         [0, 0, 0, 1.000]])

    u, s, vh = np.linalg.svd(transformation_m3[:3, :3], full_matrices=True)
    print(transformation_m3[:3, :3])
    print(s)
    apply_transfo(xv, yv, zv, transformation_m3)
    similitude(xv, yv, zv, s=5)


def generate_3d_grid():
    """
    blabla
    method: str
        Should be either 'method1' or 'method2'
    """
    x = np.arange(0, 11)
    y = np.arange(0, 11)
    z = np.arange(0, 6)
    xv, yv, zv = np.meshgrid(x, y, z)
    return xv, yv, zv


def transfo(xv, yv, zv, theta=0, omega=0, phi=0, p=0, q=0, r=0):
    """
    blabla
    method: str
        Should be either 'method1' or 'method2'
    """
    theta = np.deg2rad(theta)
    omega = np.deg2rad(omega)
    phi = np.deg2rad(phi)
    rot_x = np.matrix([[1, 0, 0, 0], [0, np.cos(theta), np.sin(theta), 0], [0, -np.sin(theta), np.cos(theta), 0], [0, 0, 0, 1]])
    rot_y = np.matrix([[np.cos(omega), 0, -np.sin(omega), 0], [0, 1, 0, 0], [np.sin(omega), 0, np.cos(omega), 0], [0, 0, 0, 1]])
    rot_z = np.matrix([[np.cos(phi), -np.sin(phi), 0, 0], [np.sin(phi), np.cos(phi), 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
    t = np.matrix([[1, 0, 0, p], [0, 1, 0, q], [0, 0, 1, r], [0, 0, 0, 0]])
    transformation = rot_x @ rot_y @ rot_z @ t
    return transformation


def apply_transfo(xv, yv, zv, transformation):
    """
    blabla
    method: str
        Should be either 'method1' or 'method2'
    """
    # fig = plt.figure(figsize=(12, 12))
    ax = plt.axes(projection='3d')
    xv_t = transformation[0, 0] * xv + transformation[0, 1] * yv + transformation[0, 2] * zv + transformation[0, 3]
    yv_t = transformation[1, 0] * xv + transformation[1, 1] * yv + transformation[1, 2] * zv + transformation[1, 3]
    zv_t = transformation[2, 0] * xv + transformation[2, 1] * yv + transformation[2, 2] * zv + transformation[2, 3]
    ax.scatter3D(xv, yv, zv)
    ax.scatter3D(xv_t, yv_t, zv_t)
    ax.set_xlabel("x axis")
    ax.set_ylabel("y axis")
    ax.set_zlabel("z axis")
    ax.set_title("3D regular grid of points with transformation M3")
    plt.show()


def similitude(xv, yv, zv, s):
    """
    blabla
    method: str
        Should be either 'method1' or 'method2'
    """
    # fig = plt.figure(figsize=(12, 12))
    ax = plt.axes(projection='3d')
    xv_t = s * xv
    yv_t = s * yv
    zv_t = s * zv
    ax.scatter3D(xv, yv, zv)
    ax.scatter3D(xv_t, yv_t, zv_t)
    ax.set_xlabel("x axis")
    ax.set_ylabel("y axis")
    ax.set_zlabel("z axis")
    ax.set_title("3D regular grid of points with scaling: s = 5")
    plt.show()



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




