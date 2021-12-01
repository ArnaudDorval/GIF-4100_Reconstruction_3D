from frame_pair_generator import get_test_frame_pairs
from laser_point_finder import get_laser_mask, get_laser_2d_position
from os import getenv
import cv2.cv2 as cv
import numpy as np

SHOW_LASER_MASK = getenv("OPTION_SHOW_LASER_MASK", "1") == "1"


def main():
    for i, (left_frame, right_frame) in enumerate(get_test_frame_pairs()):
        left_laser_mask = get_laser_mask(left_frame)
        right_laser_mask = get_laser_mask(right_frame)
        if SHOW_LASER_MASK:
            img = np.vstack((
                          np.hstack(
                              (left_frame, right_frame)
                          ),
                          np.hstack(
                              (cv.cvtColor(left_laser_mask, cv.COLOR_GRAY2BGR),
                               cv.cvtColor(right_laser_mask, cv.COLOR_GRAY2BGR))
                          ))
                      )
            # img = np.hstack(
            #                   (left_frame, right_frame)
            #               )
            cv.imshow(f"Laser masks", cv.resize(img, (800, 500)))
            cv.waitKey(1)


if __name__ == '__main__':
    main()
