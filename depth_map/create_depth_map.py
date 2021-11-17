import cv2.cv2
import numpy as np
import cv2.cv2 as cv
from pathlib import Path
import os
import matplotlib.pyplot as plt

EXTRACTED_IMAGES_PATH = Path(os.getcwd()).parent / "data" / "extracted_images"


def main():
    image_left = cv.imread(str(EXTRACTED_IMAGES_PATH / "left" / "frame_left_02600.png"), 0)
    image_right = cv.imread(str(EXTRACTED_IMAGES_PATH / "right" / "frame_right_02626.png"), 0)

    stereo = cv2.cv2.StereoBM_create(numDisparities=16, blockSize=15)
    disparity = stereo.compute(image_left, image_right)
    plt.imshow(disparity)
    plt.show()


if __name__ == '__main__':
    main()


