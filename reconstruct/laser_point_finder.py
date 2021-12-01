import numpy as np
from typing import *
from scipy.ndimage import center_of_mass

RED_THRESHOLD = 200.0

def get_laser_mask(frame: np.ndarray) -> np.ndarray:
    return ((frame[:, :, 2] > RED_THRESHOLD) * 255).astype("uint8")


def get_laser_2d_position(laser_mask: np.ndarray) -> Optional[Tuple[float, float]]:
    position = center_of_mass(laser_mask)
    if np.any(np.isnan(position)):
        return None
    else:
        return  position[1].astype("uint32"), position[0].astype("uint32")
