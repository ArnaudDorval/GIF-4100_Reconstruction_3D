import cv2
import pytesseract
from text_detection import *
import pandas as pd
import os
from datetime import datetime, timedelta


cap = cv2.VideoCapture("video_left.mp4")
success, image = cap.read()
count = 0

while success:
    old_path = "sac_timestamp/left/left_frame%d.jpg" % count
    #old_path = "sac_timestamp/right/right_frame.jpg"
    cv2.imwrite(old_path, image)  # save frame as JPEG file

    #right_time = detect_time(image)

    #new_name = "sac_timestamp/right/_" + str(right_time) + ".jpg"
    #cv2.imwrite(new_name, image)
    #os.rename(old_path, new_name)
    success, image = cap.read()
    print('Read a new frame: ', success)
    count += 1