from frame_pair_generator import get_test_frame_pairs
from laser_point_finder import get_laser_mask, get_laser_2d_position
from os import getenv
import cv2.cv2 as cv
import numpy as np

SHOW_LASER_MASK_VIDEO = getenv("OPTION_SHOW_LASER_MASK_VIDEO", "1") == "1"
SAVE_LASER_MASK_VIDEO = getenv("OPTION_SAVE_LASER_MASK_VIDEO", "1") == "1"

LASER_MASK_VIDEO_SIZE = (1400, 800)

def main():
    if SAVE_LASER_MASK_VIDEO:
        laser_mask_video = cv.VideoWriter("laser_mask.mp4", cv.VideoWriter_fourcc(*"mp4v"), 30, LASER_MASK_VIDEO_SIZE)
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

        if SHOW_LASER_MASK_VIDEO or SAVE_LASER_MASK_VIDEO:
            annotated_laser_masks = dict()
            for camera_position in ["left", "right"]:
                annotated_laser_masks[camera_position] = cv.cvtColor(laser_masks[camera_position], cv.COLOR_GRAY2BGR)
                cv.putText(annotated_laser_masks[camera_position],
                           f"{camera_position} detected laser", (50, 50), cv.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255),
                           4)
                if laser_positions[camera_position]:
                    annotated_laser_masks[camera_position] = cv.circle(annotated_laser_masks[camera_position],
                                                                       laser_positions[camera_position], 20,
                                                                       (0, 255, 0), 10)

            annotated_frames = dict()
            for camera_position in ["left", "right"]:
                annotated_frames[camera_position] = frames[camera_position].copy()
                cv.putText(annotated_frames[camera_position],
                           f"{camera_position} original", (50, 50), cv.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 4)

            img = np.vstack((
                cv.putText(np.hstack(
                    (annotated_frames["left"], annotated_frames["right"])
                ), "bla", (0, 0), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255)),
                np.hstack(
                    (annotated_laser_masks["left"],
                     annotated_laser_masks["right"])
                ))
            )

            resized_image = cv.resize(img, LASER_MASK_VIDEO_SIZE)
            if SHOW_LASER_MASK_VIDEO:
                cv.imshow(f"Laser masks", resized_image)
                cv.waitKey(1)
            if SAVE_LASER_MASK_VIDEO:
                laser_mask_video.write(resized_image)
        if SAVE_LASER_MASK_VIDEO:
            laser_mask_video.release()

if __name__ == '__main__':
    main()
