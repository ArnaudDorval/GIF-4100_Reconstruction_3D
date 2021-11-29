import os
from os import path, getcwd
from pathlib import Path
import cv2.cv2 as cv
import numpy as np
from enum import Enum

DATA_PATH = Path(os.getcwd()).parent / "data"
OUTPUT_PATH = DATA_PATH / "extracted_images_noir"
MAX_SAVED_FRAMES = 20
BLACK_THRESHOLD = 2.0
VISIBLE_THRESHOLD = 5.0
images = {"left": [], "right": []}


class SynchronizationState(Enum):
    WAITING_FOR_FIRST_BLACK_FRAME = 0
    WAITING_FOR_FIRST_LASER_FRAME = 1
    RECORDING = 2


def extract_video_images(camera_position):
    os.makedirs(OUTPUT_PATH / camera_position, exist_ok=True)

    video = cv.VideoCapture(str(DATA_PATH / f"video_{camera_position}_couleur_Trim.mp4"))
    video_frame_count = video.get(cv.CAP_PROP_FRAME_COUNT)

    success = True
    frame_number = 0
    synchronization_frame = None
    state = SynchronizationState.WAITING_FOR_FIRST_BLACK_FRAME


    while success and frame_number < video_frame_count:
        success, image = video.read()

        # State machine for synchronizing video frame numbers
        # i.e. find first frame with laser
        if state == SynchronizationState.WAITING_FOR_FIRST_BLACK_FRAME:
            if np.all(np.mean(image, (0, 1)) < BLACK_THRESHOLD):
                state = SynchronizationState.WAITING_FOR_FIRST_LASER_FRAME
        elif state == SynchronizationState.WAITING_FOR_FIRST_LASER_FRAME:
            if np.all(np.mean(image, (0, 1)) > VISIBLE_THRESHOLD):
                synchronization_frame = frame_number
                state = SynchronizationState.RECORDING
        else:
            images[camera_position].append(image)
            synchronized_frame_number = frame_number - synchronization_frame
            filename = f"frame_{camera_position}_{synchronized_frame_number:05}.png"
            # cv.imwrite(str(OUTPUT_PATH / camera_position / filename), image)
            print(f"Wrote image {filename}.")

        frame_number += 1


def create_side_by_side_video():
    out = cv.VideoWriter(str(OUTPUT_PATH / "side-by-side.mp4"), cv.VideoWriter_fourcc(*"mp4v"), 30, (1280, 720 * 2))

    for i in range(min(len(images["left"]), len(images["right"]))):
        left_image = images["left"][i]
        right_image = images["right"][i]
        image = cv.vconcat([left_image, right_image])
        out.write(image)
    out.release()


def main():
    for camera_position in ["left", "right"]:
        extract_video_images(camera_position)
    create_side_by_side_video()


if __name__ == '__main__':
    main()
