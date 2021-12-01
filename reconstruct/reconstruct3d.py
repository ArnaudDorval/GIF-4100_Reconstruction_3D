from math import tan, pi

# https://www.logitech.com/en-ca/products/webcams/c270-hd-webcam.960-000694.html#specs
VIEW_ANGLE = 47.9367

DISTANCE_BETWEEN_CAMERAS = 50  # millimeters
FOCAL_LENGTH = 5  # millimeters TODO: change this to real value from camera matrix


def deg2rad(deg):
    return deg * pi / 180


def compute_distance(left_position: tuple, right_position: tuple, image_width) -> tuple:
    # From section III.E of Design of a Laser Pointer Follower Robot

    b = DISTANCE_BETWEEN_CAMERAS
    x0 = image_width
    phi_0 = deg2rad(VIEW_ANGLE)
    x1 = left_position[0] - (image_width // 2)
    x2 = right_position[0] - (image_width // 2)
    d = b * x0 / (2 * tan(phi_0 / 2) * (x1 - x2))

    return d
