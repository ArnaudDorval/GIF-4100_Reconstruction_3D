import cv2.cv2
import numpy as np
import cv2.cv2 as cv
from pathlib import Path
import os
import matplotlib.pyplot as plt
from root import ROOT_PATH
import pickle
import sys
import cv2.cv2 as cv
from mpl_toolkits.mplot3d import Axes3D
from constants import EXTRACTED_IMAGES_PATH

# make sure pickle has access to calibration_var
# see https://stackoverflow.com/a/54195619/6233186
sys.path.append(str(ROOT_PATH / "Calibration"))




def main():
    image_left = cv.imread(str(EXTRACTED_IMAGES_PATH / "left" / "frame_left_01600.png"))
    image_right = cv.imread(str(EXTRACTED_IMAGES_PATH / "right" / "frame_right_01616.png"))

    # Red filter
    lowerb = np.array([0, 0, 120])
    upperb = np.array([100, 100, 255])
    image_left = cv2.inRange(image_left, lowerb, upperb)
    image_right = cv2.inRange(image_right, lowerb, upperb)

    cv.imshow("two images", cv2.addWeighted(image_left, 0.75, image_right, 0.25, 0.0))
    cv.waitKey(0)

    stereo = cv2.cv2.StereoBM_create(numDisparities=16, blockSize=9)
    disparity = stereo.compute(image_left, image_right)

    cv2.imshow("disparity", disparity)
    cv2.waitKey(0)

    # 3d reconstruction
    camera_calibrations = dict()

    for camera_name in ["camera_A", "camera_B"]:
        with open(ROOT_PATH / "Calibration" / camera_name / "calibration_camera_.dat", "rb") as f:
            camera_calibrations[camera_name] = pickle.load(f)

    print(camera_calibrations)
    print(camera_calibrations["camera_A"].cameraMatrix)
    print(camera_calibrations["camera_B"].cameraMatrix)
    adapted_camera_matrix = np.eye(4)
    adapted_camera_matrix[0:3, 0:3] = camera_calibrations["camera_A"].cameraMatrix
    points3d = cv.reprojectImageTo3D(disparity, adapted_camera_matrix)
    colors = cv.cvtColor(image_left, cv.COLOR_BGR2RGB)
    mask = disparity > disparity.min()

    output_points = points3d[mask]
    output_colors = colors[mask].astype("float") / 255

    figure = plt.figure()
    axes = Axes3D(figure)
    axes.scatter(output_points[:, 0], output_points[:, 1], output_points[:, 2], s=1, c=output_colors)
    plt.show()


if __name__ == '__main__':
    main()


