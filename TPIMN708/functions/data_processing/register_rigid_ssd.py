import numpy as np
import scipy

from functions.data_processing.register_translation_ssd import SSD
from functions.data_processing.rotate_image import rotate_image
from functions.data_processing.translate_image import translate_image
from matplotlib import pyplot as plt
from functions.data_processing.rigid_transformation import rigid_transformation

def SSD_fun(x, I, J):
    """Computing the sum of squared differences (SSD) between two images and return function"""
    # x = [theta, p , q]
    if I.shape != J.shape:
        print("Images don't have the same shape.")
        return
    #I_r_p_q = rigid_transformation(I, x[0], x[1], x[2])
    return lambda x: np.sum((np.array(rigid_transformation(I, x[0], x[1], x[2]), dtype=np.float32) - np.array(J, dtype=np.float32)) ** 2)

def SSD(I, J):
    """Computing the sum of squared differences (SSD) between two images."""
    # x = [theta, p , q]
    if I.shape != J.shape:
        print("Images don't have the same shape.")
        return
    return np.sum((np.array(I, dtype=np.float32) - np.array(J, dtype=np.float32)) ** 2)


def register_rigid_ssd(I, J, epsilon=10**(-8)):
    """Register image with minimization of SSD with gradient descent."""
    theta = 0
    p, q = 0, 0
    I_r_p_q = rigid_transformation(I, theta, p , q)
    print_image(I, I_r_p_q, J)
    ssd_v = []

    # original grid
    x = np.arange(0, I.shape[0])
    y = np.arange(0, I.shape[1])
    xv, yv = np.meshgrid(x, y)

    for n in range(100):
        #print_image(I, I_r_p_q, J)
        dSSD_dtheta = 2 * sum(sum((I_r_p_q - J) * (
                    np.gradient(I, axis=0) * (-xv * np.sin(theta) - yv * np.cos(theta)) + np.gradient(I, axis=1) * (
                        xv * np.cos(theta) - yv * np.sin(theta)))))
        dSSD_dp = 2 * sum(sum((I_r_p_q - J) * np.gradient(I_r_p_q, axis=0)))
        dSSD_dq = 2 * sum(sum((I_r_p_q - J) * np.gradient(I_r_p_q, axis=1)))
        p = p + epsilon * dSSD_dp
        q = q + epsilon * dSSD_dq
        theta = theta + 0.1*epsilon * dSSD_dtheta
        I_r_p_q = rigid_transformation(I, theta, p , q)
        print("SSD: {}, change in theta: {} ".format(SSD(I_r_p_q, J), theta))
        ssd_v.append(SSD(I_r_p_q, J))
    print_image(I, I_r_p_q, J)
    plt.plot(ssd_v)
    plt.title("SSD in function of iteration")
    plt.ylabel("SSD")
    plt.xlabel("iteration")
    plt.show()

def print_image(I, I_t, J):
    """print image to visualize results of SSD minimization"""
    fig, ax = plt.subplots(1, 3, figsize=(15, 5))
    ax[0].imshow(I)
    ax[0].set_title("Original image")
    ax[1].imshow(I_t)
    ax[1].set_title("Registered image")
    ax[2].imshow(J)
    ax[2].set_title("Destination image")
    plt.show()


def register_rigid_ssd_min(I, J, epsilon=10**(-8)):
    """Register image with minimization of SSD with Powell method."""
    theta = 0
    p, q = 0, 0
    x0 = [0,0,0]
    x = []
    I_r_p_q = rigid_transformation(I, theta, p , q)
    print_image(I, I_r_p_q, J)
    a = scipy.optimize.minimize(SSD_fun(x, I, J), x0, method='Powell', tol=10**(-8))
    print(a)
    print(a.x)
    I_r_p_q = rigid_transformation(I, a.x[0], a.x[1], a.x[2])
    print_image(I, I_r_p_q, J)
