from math import tan, pi
from typing import *
from root import ROOT_PATH
import pickle
import sys

# https://www.logitech.com/en-ca/products/webcams/c270-hd-webcam.960-000694.html#specs
VIEW_ANGLE = 47.9367

DISTANCE_BETWEEN_CAMERAS = 50  # millimeters
FOCAL_LENGTH = 5  # millimeters TODO: change this to real value from camera matrix
XY_SCALE_FACTOR_PIXEL_TO_MM = 1 # 7 / 1280  # (~7 mm image plane width / 1280 px) TODO: Change this for real value
MAX_DISTANCE = 2000 # TODO: Find good threshold

# make sure pickle has access to calibration_var
# see https://stackoverflow.com/a/54195619/6233186
sys.path.append(str(ROOT_PATH / "Calibration"))

def deg2rad(deg):
    return deg * pi / 180


def compute_distance(left_position: tuple, right_position: tuple, image_width) -> Optional[tuple]:
    # From section III.E of Design of a Laser Pointer Follower Robot

    b = DISTANCE_BETWEEN_CAMERAS
    x0 = image_width
    phi_0 = deg2rad(VIEW_ANGLE)
    x1 = left_position[0] - (x0 // 2)
    x2 = right_position[0] - (x0 // 2)
    d = b * x0 / (2 * tan(phi_0 / 2) * (x1 - x2))

    if abs(d) > MAX_DISTANCE:
        return None

    return left_position[0] * XY_SCALE_FACTOR_PIXEL_TO_MM, left_position[1] * XY_SCALE_FACTOR_PIXEL_TO_MM, d


def get_3d_position(laser_positions: Dict[str, tuple]) -> tuple:
    # unused

    camera_calibrations = dict()

    for camera_name in ["camera_A", "camera_B"]:
        with open(ROOT_PATH / "Calibration" / camera_name / "calibration_camera_.dat", "rb") as f:
            camera_calibrations[camera_name] = pickle.load(f)
    print(camera_calibrations)


