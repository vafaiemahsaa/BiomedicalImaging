import numpy as np

from functions.data_processing.register_translation_ssd import SSD
from functions.data_processing.rotate_image import rotate_image
from matplotlib import pyplot as plt



def register_rotation_ssd_m(I,J):
    I = np.float32(I)
    J = np.float32(J)
    theta = -180
    ssd = [float('inf')]
    rotation = []
    while theta < 180:
        I_R = rotate_image(I, theta)
        ssd.append(SSD(I_R, J))
        if ssd[-1] < ssd[-2]:
            theta = theta + .6
        else:
            theta = theta + .3
        rotation.append(theta)
    print(rotation[ssd.index(min(ssd))])
    # print(ssd_y)
    plt.plot(rotation, ssd[1:])
    plt.show()





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


def register_rotation_ssd(I, J, epsilon=0.5 * 10**(-8)):
    theta = 0
    I_r = rotate_image(I, theta)
    print_image(I, I_r, J)
    ssd_v = []

    # original grid
    x = np.arange(0, I.shape[0])
    y = np.arange(0, I.shape[1])
    xv, yv = np.meshgrid(x, y)

    for n in range(100):
        dSSD_dtheta = 2 * sum(sum((I_r - J) * (
                    np.gradient(I, axis=0) * (-xv * np.sin(theta) - yv * np.cos(theta)) + np.gradient(I, axis=1) * (
                        xv * np.cos(theta) - yv * np.sin(theta)))))
        print(dSSD_dtheta)
        theta = theta + epsilon * dSSD_dtheta
        I_r = rotate_image(I, theta)
        print("SSD: {}, change in theta: {} ".format(SSD(I_r, J), theta))
        ssd_v.append(SSD(I_r, J))
    print_image(I, I_r, J)
    plt.plot(ssd_v)
    plt.title("SSD in function of iteration")
    plt.ylabel("SSD")
    plt.xlabel("iteration")
    plt.show()

def print_image(I, I_t, J):
    fig, ax = plt.subplots(1, 3, figsize=(15, 5))
    ax[0].imshow(I)
    ax[0].set_title("Original image")
    ax[1].imshow(I_t)
    ax[1].set_title("Registered image")
    ax[2].imshow(J)
    ax[2].set_title("Destination image")
    plt.show()
