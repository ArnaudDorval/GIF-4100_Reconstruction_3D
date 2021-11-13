import os
import numpy as np
import cv2

filename_0 = "video_0a.avi"
filename_1 = "video_0b.avi"

fps = 24.0
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


cap_0 = cv2.VideoCapture(1)
out_0 = cv2.VideoWriter(filename_0, get_video_type(filename_0), 25, get_dims(cap_0, res))
cap_1 = cv2.VideoCapture(2)
out_1 = cv2.VideoWriter(filename_1, get_video_type(filename_1), 25, get_dims(cap_1, res))

while(True):
    ret0, frame0 = cap_0.read()
    ret1, frame1 = cap_1.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame0, cv2.COLOR_BGR2GRAY)

    if (ret0):
        out_0.write(frame0)
        cv2.imshow('cam 0 ', frame0)
    if (ret1):
        out_1.write(frame1)
        cv2.imshow('cam 1 ', frame1)

    #enregistrer vid

    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

cap_0.release()
out_0.release()
cap_1.release()
out_1.release()
cv2.destroyAllWindows()