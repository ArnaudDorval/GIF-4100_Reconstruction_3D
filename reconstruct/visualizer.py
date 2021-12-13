import cv2.cv2 as cv
import numpy as np
from plyfile import PlyData, PlyElement
from typing import *


LASER_MASK_VIDEO_SIZE = (1400, 800)


def visualize(color_image, frames, laser_masks, laser_positions, *, show_laser_mask_video, save_laser_mask_video):
    if save_laser_mask_video:
        laser_mask_video = cv.VideoWriter("laser_mask.mp4", cv.VideoWriter_fourcc(*"mp4v"), 30, LASER_MASK_VIDEO_SIZE)

    # Original frames
    annotated_frames = dict()
    for camera_position in ["left", "right"]:
        annotated_frames[camera_position] = frames[camera_position].copy()
        cv.putText(annotated_frames[camera_position],
                   f"{camera_position} original", (50, 50), cv.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 4)

    # Laser-detected frames
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

    img = np.vstack((
        np.hstack((color_image, color_image)),
        cv.putText(np.hstack(
            (annotated_frames["left"], annotated_frames["right"])
        ), "bla", (0, 0), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255)),
        np.hstack(
            (annotated_laser_masks["left"],
             annotated_laser_masks["right"])
        ))
    )

    resized_image = cv.resize(img, LASER_MASK_VIDEO_SIZE)
    if show_laser_mask_video:
        cv.imshow(f"Laser masks", resized_image)
        cv.waitKey(1)
    if save_laser_mask_video:
        laser_mask_video.write(resized_image)
    if save_laser_mask_video:
        laser_mask_video.release()


def create_ply_file_from_point_cloud(points: List[tuple], color_image: np.ndarray, filepath):
    # https://github.com/dranjan/python-plyfile
    updated_points = []
    for point in points:
        color = color_image[point[1], point[0]]
        updated_points.append((*point, *color))
    vertices = np.array(updated_points,
                        dtype=[("x", "f4"), ("y", "f4"), ("z", "f4"),
                               ("diffuse_red", "u1"), ("diffuse_green", "u1"), ("diffuse_blue", "u1")])
    element = PlyElement.describe(vertices, "vertex")
    PlyData([element], text=True).write(filepath)
