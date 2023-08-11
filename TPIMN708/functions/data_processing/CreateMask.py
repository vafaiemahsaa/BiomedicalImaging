import nibabel as nib
import numpy as np


def CreateB0Mask(dmri):
    dmri_data = dmri.get_data()
    b0 = dmri_data[..., 0]
    print(dmri_data.shape[-1])
    #
    print(dmri_data.shape)
    # b0nifti = nib.Nifti1Image(b0, dmri.affine)
    # nib.save(b0nifti, 'Data/b0_mask.nii.gz')
    # use FSL BET to remove the background
    Mask = nib.load('Data/b0_mask_brain.nii').get_data()
    masked_dmri = np.empty(dmri_data.shape)
    for i in range(dmri_data.shape[-1]):
        masked_dmri[..., i] = dmri_data[..., i] * Mask[...]
    return masked_dmri, Mask


def CreateWMmask(b0Mask, FA, dmri):
    fa_temp = (FA > .20)
    # print(fa_temp.shape)
    # print(b0Mask.shape)
    wm_mask = np.zeros((dmri.shape[0], dmri.shape[1], dmri.shape[2]), dtype=np.int8)
    wmNonZeroList = []
    for i in range(fa_temp.shape[0]):
        for j in range(fa_temp.shape[1]):
            for k in range(fa_temp.shape[2]):
                wmNonZeroList.append([i, j, k])
                if fa_temp[i, j, k] > 0:
                    if b0Mask[i, j, k] > 0:
                        wm_mask[i, j, k] = 1;

    # wmnifti = nib.Nifti1Image(wm_mask, dmri.affine)
    # nib.save(wmnifti, 'Data/wm_mask.nii.gz')

    return wm_mask, wmNonZeroList
