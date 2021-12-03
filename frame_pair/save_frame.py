import cv2
import pytesseract
from text_detection import *
import pandas as pd
import os
from datetime import datetime, timedelta

direction = "right"

file_name = direction + "_image.csv"
df = pd.read_csv ("./botte_1/" + direction +"_times.csv")

cap = cv2.VideoCapture("./botte_1/video_" + direction + ".mp4")
success, image = cap.read()
count = 0

property_id = int(cv2.CAP_PROP_FRAME_COUNT)
length = int(cv2.VideoCapture.get(cap, property_id))

print( "nb frame : " + str(length) )
l = len(str(length))

list_img = []

while success:

    name_nb = str(count)
    while len(name_nb) < l:
        name_nb = "0" + name_nb

    old_path = "botte_1/right/" + direction + "_frame" + name_nb +".jpg"
    cv2.imwrite(old_path, image)  # save frame as JPEG file

    list_img.append(direction + "_frame" + name_nb +".jpg")

    success, image = cap.read()
    count += 1

print("done, number of images : " + str(count))
df['filename'] = list_img
df.to_csv(file_name, encoding='utf-8', index=False)