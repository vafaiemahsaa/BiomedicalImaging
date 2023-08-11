import nibabel as nib
import numpy as np
import random
from functions.ADCandFA import returnD_


def returnAngle(t1, t2):
    t1_u = t1 / np.linalg.norm(t1)
    t2_u = t2 / np.linalg.norm(t2)
    return np.arccos(np.clip(np.dot(t1_u, t2_u), -1.0, 1.0))


def tracking(T, wm_mask, wmNonZeroList):
    """"""
    max_angle = np.pi / 3
    streamlines = []
    for i in range(100000):
        seed = random.choice(wmNonZeroList)
        x = int(seed[0])
        y = int(seed[1])
        z = int(seed[2])

        streamline = []

        D = T[x, y, z]
        eig, vec = np.linalg.eig(returnD_(D))

        peak = np.argmax(eig)
        track = vec[:, peak]
        track_temp = track

        temp_x = x
        temp_y = y
        temp_z = z
        while ((wm_mask[x, y, z] == 1) and (
                returnAngle(track_temp, track) >= np.pi - max_angle
                or returnAngle(track_temp, track) <= max_angle)):
            streamline.append([temp_x, temp_y, temp_z])
            if returnAngle(track_temp, track) >= np.pi - max_angle:
                track = track * -1
            # print(track[0])
            temp_x += track[0] * .5
            temp_y += track[1] * .5
            temp_z += track[2] * .5

            x = int(np.round(temp_x))
            y = int(np.round(temp_y))
            z = int(np.round(temp_z))

            if  x < wm_mask.shape[0] and y < wm_mask.shape[1] and z < wm_mask.shape[2]:
                D = T[x, y, z]
                eig, vec = np.linalg.eig(returnD_(D))
                track_temp = track
                peak = np.argmax(eig)
                track = vec[:, peak]
            else:
                break

        streamline.insert(0, [temp_x, temp_y, temp_z])

        if len(streamline) > 8:
            streamlines.append(np.array(streamline))
    return streamlines
