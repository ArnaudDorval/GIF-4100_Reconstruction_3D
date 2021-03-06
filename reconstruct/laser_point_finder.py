import numpy as np
from typing import *
from scipy.ndimage import center_of_mass
import cv2.cv2 as cv

RED_THRESHOLD = 200.0

def get_laser_mask(frame: np.ndarray) -> np.ndarray:
    # return ((frame[:, :, 2] > RED_THRESHOLD) * 255).astype("uint8")
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    lower_red = np.array([7, 0, 95])
    upper_red = np.array([170, 255, 255])
    mask = cv.inRange(hsv, lower_red, upper_red)
    return mask


def get_laser_2d_position(laser_mask: np.ndarray) -> Optional[Tuple[float, float]]:
    position = center_of_mass(laser_mask)
    if np.any(np.isnan(position)):
        return None
    else:
        # TODO: Maybe remove approximation
        return  position[1].astype("uint32"), position[0].astype("uint32")
