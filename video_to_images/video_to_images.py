import os
from os import path, getcwd
from pathlib import Path
import cv2.cv2 as cv

DATA_PATH = Path(os.getcwd()).parent / "data"
OUTPUT_PATH = DATA_PATH / "extracted_images"
MAX_SAVED_FRAMES = 20


def extract_video_images(camera_position):
    os.makedirs(OUTPUT_PATH / camera_position, exist_ok=True)

    video = cv.VideoCapture(str(DATA_PATH / f"video_{camera_position}.avi"))
    video_frame_count = video.get(cv.CAP_PROP_FRAME_COUNT)

    success = True
    frame_number = 0
    while success and frame_number < video_frame_count:
        success, image = video.read()

        if frame_number % (video_frame_count // MAX_SAVED_FRAMES) == 0:
            filename = f"frame_{camera_position}_{frame_number:05}.png"
            cv.imwrite(str(OUTPUT_PATH / camera_position / filename), image)
            print(f"Wrote image {filename}.")

        frame_number += 1


def main():
    for camera_position in ["left", "right"]:
        extract_video_images(camera_position)


if __name__ == '__main__':
    main()
