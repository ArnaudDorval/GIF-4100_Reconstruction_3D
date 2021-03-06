import os
import numpy as np
import cv2
from multiprocessing import Process
from datetime import datetime
import pandas as pd

fps = 30
res = '720p'

# Standard Video Dimensions Sizes
STD_DIMENSIONS = {
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
        width, height = STD_DIMENSIONS[res]
    ## change the current caputre device
    ## to the resulting resolution
    change_res(cap, width, height)
    return width, height


# Video Encoding, might require additional installs
# Types of Codes: http://www.fourcc.org/codecs.php
VIDEO_TYPE = {
    'avi': cv2.VideoWriter_fourcc(*'XVID'),
    # 'mp4': cv2.VideoWriter_fourcc(*'H264'),
    'mp4': cv2.VideoWriter_fourcc(*'XVID'),
}


def get_video_type(filename):
    filename, ext = os.path.splitext(filename)
    if ext in VIDEO_TYPE:
        return VIDEO_TYPE[ext]
    return VIDEO_TYPE['avi']


def webcam_video(p_camera):
    cap = cv2.VideoCapture(p_camera)
    name = ""
    if (p_camera == 0):
        name = 'laptop'
    elif (p_camera == 1):
        name = 'left'
    else:
        name = 'right'

    filename = "video_" + name + ".mp4"

    out = cv2.VideoWriter(filename, get_video_type(filename), fps, get_dims(cap, res))
    df_arr = []

    while (True):
        ret, frame = cap.read()
        if ret == True:
            font = cv2.FONT_HERSHEY_SCRIPT_SIMPLEX
            t = datetime.now()
            dt = str(str(t.hour) + ':' + str(t.minute) + ':' + str(t.second) + '.' + str(t.microsecond))

            df_arr.append(dt)

            frame = cv2.putText(frame, dt,
                                (1000, 700),
                                font, 1,
                                (255, 255, 255),
                                4, cv2.LINE_8)
            out.write(frame)
            cv2.imshow(name, frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                df = pd.DataFrame(df_arr, columns=['time'])
                df.to_csv(name + "_times.csv", encoding='utf-8', index=False)
                break
        else:
            break
    cap.release()
    out.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    p1 = Process(target=webcam_video, args=(1,))
    p2 = Process(target=webcam_video, args=(2,))
    # T = Thread(target=run, args=("Ayla",))
    p1.start()
    p2.start()

    p1.join()
    p2.join()