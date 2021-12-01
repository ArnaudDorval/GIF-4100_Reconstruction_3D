from frame_pair_generator import get_test_frame_pairs
from laser_point_finder import get_laser_mask, get_laser_2d_position
from os import getenv
import cv2.cv2 as cv
import numpy as np

SHOW_LASER_MASK = getenv("OPTION_SHOW_LASER_MASK", "1") == "1"


def main():
    for i, (left_frame, right_frame) in enumerate(get_test_frame_pairs()):
        frames = {
            "left": left_frame,
            "right": right_frame
        }
        laser_masks = dict()
        laser_positions = dict()
        for camera_position in ["left", "right"]:
            laser_masks[camera_position] = get_laser_mask(frames[camera_position])
            laser_positions[camera_position] = get_laser_2d_position(laser_masks[camera_position])

        if SHOW_LASER_MASK:
            annotated_laser_masks = dict()
            for camera_position in ["left", "right"]:
                annotated_laser_masks[camera_position] = cv.cvtColor(laser_masks[camera_position], cv.COLOR_GRAY2BGR)
                if laser_positions[camera_position]:
                    annotated_laser_masks[camera_position] = cv.circle(annotated_laser_masks[camera_position],
                                                                       laser_positions[camera_position], 20,
                                                                       (0, 255, 0), 10)

            img = np.vstack((
                np.hstack(
                    (frames["left"], frames["right"])
                ),
                np.hstack(
                    (annotated_laser_masks["left"],
                     annotated_laser_masks["right"])
                ))
            )

            cv.imshow(f"Laser masks", cv.resize(img, (1400, 800)))
            cv.waitKey(1)


if __name__ == '__main__':
    main()
