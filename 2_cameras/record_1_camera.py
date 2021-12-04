import os
import numpy as np
import cv2
from datetime import datetime
import pandas as pd

filename = "ttt.avi"
fps = 30
res = '720p'

# Standard Video Dimensions Sizes
STD_DIMENSIONS =  {
    "480p": (640, 480),
    "720p": (1280, 720),
    "1080p": (1920, 1080),
    "4k": (3840, 2160),
}

# Set resolution for the video capture
def change_res(cap, width, height):
    cap.set(3, width)
    cap.set(4, height)

# grab resolution dimensions and set video capture to it.
def get_dims(cap, res='720p'):
    width, height = STD_DIMENSIONS["480p"]
    if res in STD_DIMENSIONS:
        width,height = STD_DIMENSIONS[res]
    ## change the current caputre device
    ## to the resulting resolution
    change_res(cap, width, height)
    return width, height

# Video Encoding, might require additional installs
# Types of Codes: http://www.fourcc.org/codecs.php
VIDEO_TYPE = {
    'avi': cv2.VideoWriter_fourcc(*'XVID'),
    #'mp4': cv2.VideoWriter_fourcc(*'H264'),
    'mp4': cv2.VideoWriter_fourcc(*'XVID'),
}

def get_video_type(filename):
    filename, ext = os.path.splitext(filename)
    if ext in VIDEO_TYPE:
      return  VIDEO_TYPE[ext]
    return VIDEO_TYPE['avi']


cap = cv2.VideoCapture(0)
out = cv2.VideoWriter(filename, get_video_type(filename), fps, get_dims(cap, res))


df_arr = []

while(True):
    # capture frame-by-frame
    ret, frame = cap.read()
    if ret:

        font = cv2.FONT_HERSHEY_SCRIPT_SIMPLEX
        t = datetime.now()
        dt = str(str(t.hour) + ':' + str(t.minute) + ':' + str(t.second) + '.' + str(t.microsecond))
        df_arr.append(dt)
        frame = cv2.putText(frame, dt,
                            (1000, 700),
                            font, 1,
                            (255, 255, 255),
                            4, cv2.LINE_8)
        #enregistrer vid
        out.write(frame)

        #display resulting frame

        cv2.imshow('frame', frame)
        if cv2.waitKey(20) & 0xFF == ord('q'):
            df = pd.DataFrame(df_arr, columns=['time'])
            df.to_csv("ttt_times", encoding='utf-8', index=False)
            break

cap.release()
out.release()
cv2.destroyAllWindows()