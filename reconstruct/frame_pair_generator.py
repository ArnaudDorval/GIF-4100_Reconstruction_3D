from typing import *
import numpy as np
import cv2.cv2 as cv
from constants import DATA_PATH
import pandas as pd


def get_test_frame_pairs() -> Generator[Tuple[np.ndarray, np.ndarray], None, None]:
    frame_left_index = 473 + 109
    frame_right_index = 462 + 109
    max_frame_left_index = 3541
    max_frame_right_index = 3606

    while frame_left_index <= max_frame_left_index and frame_right_index <= max_frame_right_index:
        image_left = cv.imread(str(DATA_PATH / "extracted_images_sac" / "left" / f"frame_left_{frame_left_index:05}.png"))
        image_right = cv.imread(str(DATA_PATH / "extracted_images_sac" / "right" / f"frame_right_{frame_right_index:05}.png"))
        yield image_left, image_right

        frame_left_index += 1
        frame_right_index += 1


def get_frame_pairs(video_name) -> Generator[Tuple[np.ndarray, np.ndarray], None, None]:
    df = pd.read_csv(DATA_PATH / video_name / "pair_image.csv")
    for _, row in df.iterrows():
        image_left = cv.imread(str(DATA_PATH / video_name / "left" / row["left"]))
        image_right = cv.imread(str(DATA_PATH / video_name / "right" / row["right"]))
        yield image_left, image_right
