import numpy as np


def RMS(img,from_nifit):
    if from_nifit:
        img_data = np.asarray(img.get_fdata())
    else:
        img_data=np.array(img)

    # image_data = pyfits.getdata(image,ignore_missing_end=True)
    rms = img_data.std() / img_data.mean()
    return rms
