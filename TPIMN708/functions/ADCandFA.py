import numpy as np
import nibabel as nib


def returnD_(D):
    return [[D[0], D[1], D[2]],
            [D[1], D[3], D[4]],
            [D[2], D[4], D[5]]]


def ADCandFAcalculator(T, b0Mask):
    """ Calculation of the ADC and the FA of a 3D matrix comprising
    diffusion tensors at each index.
    """

    # Initialization of output variables
    ADC = np.zeros(T.shape[:3])
    FA = np.zeros(T.shape[:3])

    for i in range(b0Mask.shape[0]):
        for j in range(b0Mask.shape[1]):
            for k in range(b0Mask.shape[2]):
                if b0Mask[i, j, k] != 0:
                    D = T[i,j,k]
                    eig, vec = np.linalg.eig(returnD_(D))
                    ADC[i, j, k] = eig.sum() / 3
                    FA[i, j, k] = np.sqrt(3 / 2 * ((eig - eig.mean()) ** 2).sum() /
                                          (eig ** 2).sum())
    return ADC.astype(float), FA.astype(float)



