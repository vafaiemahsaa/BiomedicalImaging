
import numpy as np
import matplotlib.image as mpimg


def Michelson_Contrast(img,from_nifit):
    # compute min and max of image
    if from_nifit:
        img_data=np.asarray(img.get_fdata())

    else:
        img_data=np.array(img)

    min = np.min(img_data)
    max = np.max(img_data)


    # compute contrast
    contrast = (max - min) / (max + min)
    return contrast
