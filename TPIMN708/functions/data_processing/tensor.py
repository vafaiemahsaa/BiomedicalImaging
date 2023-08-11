import math

import numpy as np
import scipy


def tensor(dmri_data, gradients, B0Mask):
    """Estimation of tensors by least squares method. [Dxx, Dxy, Dxz, Dyy, Dyz, Dzz]"""

    b0Mask = np.array(B0Mask)
    gradients = np.genfromtxt(gradients)[1:]
    S0 = dmri_data[..., 0]
    S = dmri_data[..., 1:]
    tensor = np.zeros((b0Mask.shape[0], b0Mask.shape[1], b0Mask.shape[2], 6))

    B = np.array([gradients[:, 0] ** 2, gradients[:, 0] * gradients[:, 1],gradients[:, 0] * gradients[:, 2], gradients[:, 1] ** 2,gradients[:, 1] * gradients[:, 2], gradients[:, 2] ** 2]).T

    for i in range(b0Mask.shape[0]):
        for j in range(b0Mask.shape[1]):
            for k in range(b0Mask.shape[2]):
                if b0Mask[i, j, k] != 0:
                    x = - ((1 / gradients[:, 3].astype(float)) * (
                        np.log(S[i, j, k].astype(float) / S0[i, j, k].astype(float))))
                    tensor[i, j, k] = np.dot(scipy.linalg.pinv(B), x)

    tensor[np.isinf(tensor) | np.isnan(tensor)] = 0

    return tensor
