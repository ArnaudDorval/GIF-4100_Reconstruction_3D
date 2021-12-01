from frame_pair_generator import get_test_frame_pairs
from laser_point_finder import get_laser_mask, get_laser_2d_position
from os import getenv
from visualizer import visualize

SHOW_LASER_MASK_VIDEO = getenv("OPTION_SHOW_LASER_MASK_VIDEO", "1") == "1"

# TODO: not working now (using Sharex instead)
SAVE_LASER_MASK_VIDEO = getenv("OPTION_SAVE_LASER_MASK_VIDEO", "0") == "1"


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

        visualize(frames, laser_masks, laser_positions, show_laser_mask_video=SHOW_LASER_MASK_VIDEO,
                  save_laser_mask_video=SAVE_LASER_MASK_VIDEO)


if __name__ == '__main__':
    main()