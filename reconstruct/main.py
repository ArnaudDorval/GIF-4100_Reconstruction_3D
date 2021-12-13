from frame_pair_generator import get_test_frame_pairs, get_frame_pairs
from laser_point_finder import get_laser_mask, get_laser_2d_position
from os import getenv
from reconstruct3d import get_3d_position, compute_distance
from visualizer import visualize, create_ply_file_from_point_cloud

SHOW_LASER_MASK_VIDEO = getenv("OPTION_SHOW_LASER_MASK_VIDEO", "1") == "1"
SAVE_LASER_MASK_VIDEO = getenv("OPTION_SAVE_LASER_MASK_VIDEO", "0") == "1"
# VIDEO_NAME = "botte_2"
# RECONSTRUCTION_IMAGE_INDEX_START = 446
# RECONSTRUCTION_IMAGE_INDEX_END = 4804
VIDEO_NAME = "botte_3"
RECONSTRUCTION_IMAGE_INDEX_START = 900 # 816
RECONSTRUCTION_IMAGE_INDEX_END = 5000


def main():
    point_cloud_3d = []

    color_image = None
    for i, (left_frame, right_frame) in enumerate(get_frame_pairs(VIDEO_NAME)):
        if i < 693:  # for botte_3
        # if i == 0: # for botte_2
            color_image = left_frame

        if i < RECONSTRUCTION_IMAGE_INDEX_START:
           continue
        if i > RECONSTRUCTION_IMAGE_INDEX_END:
           break

        frames = {
            "left": left_frame,
            "right": right_frame
        }
        laser_masks = dict()
        laser_positions = dict()
        for camera_position in ["left", "right"]:
            laser_masks[camera_position] = get_laser_mask(frames[camera_position])
            laser_positions[camera_position] = get_laser_2d_position(laser_masks[camera_position])

        if laser_positions["left"] and laser_positions["right"]:
            point = compute_distance(laser_positions["left"], laser_positions["right"], 1280)
            if point:
                point_cloud_3d.append(point)

        visualize(color_image, frames, laser_masks, laser_positions, show_laser_mask_video=SHOW_LASER_MASK_VIDEO,
                  save_laser_mask_video=SAVE_LASER_MASK_VIDEO)

    create_ply_file_from_point_cloud(point_cloud_3d, color_image, "out.ply")


if __name__ == '__main__':
    main()
