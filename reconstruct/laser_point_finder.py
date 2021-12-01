import numpy as np
from typing import *

RED_THRESHOLD = 200.0

def get_laser_mask(frame: np.ndarray) -> np.ndarray:
    return ((frame[:, :, 2] > RED_THRESHOLD) * 255).astype("uint8")


def get_laser_2d_position(laser_mask: np.ndarray) -> Tuple[float, float]:
    pass
