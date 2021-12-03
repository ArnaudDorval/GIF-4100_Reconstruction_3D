import cv2
import pytesseract
from text_detection import *
import pandas as pd
import os
from datetime import datetime, timedelta

left_cap = cv2.VideoCapture("video_left.mp4")
right_cap = cv2.VideoCapture("video_right.mp4")

property_id = int(cv2.CAP_PROP_FRAME_COUNT)
left_length = int(cv2.VideoCapture.get(left_cap, property_id))
right_length = int(cv2.VideoCapture.get(right_cap, property_id))

print( "nb left frame : " + str(left_length) )
print( "nb right frame : " + str(right_length) )

# extract first_frame
rval, frame = left_cap.read()
cv2.imwrite('left_frame.jpg', frame)

left_time_stamp, bidon = detect_time('left_frame.jpg')
print("left time : " + str(left_time_stamp))

# extract first_frame
rval, frame = right_cap.read()
cv2.imwrite('right_frame.jpg', frame)


right_time_stamp, bidon = detect_time('right_frame.jpg')
print("right time : " + str(right_time_stamp))

if(left_time_stamp < right_time_stamp):
    a = right_time_stamp - left_time_stamp
else:
    a = left_time_stamp - right_time_stamp

left_success, left_image = left_cap.read()
left_count = 0
smallest_diff = timedelta(hours=3, minutes=3, seconds=3)

list_pair = []
best_left = ""
best_right = ""
df = pd.DataFrame(columns=['time', 'left', 'right'])

while left_success:
    left_path = "sac_timestamp/left/left_frame%d.jpg" % left_count
    cv2.imwrite(left_path, left_image)     # save frame as JPEG file

    right_success, right_image = right_cap.read()
    right_count = 0
    smallest_diff = timedelta(hours=3, minutes=3, seconds=3)
    while right_success:
        right_path = "sac_timestamp/right/right_frame%d.jpg" % right_count
        cv2.imwrite(right_path, right_image)  # save frame as JPEG file

        left_time, s1 = detect_time(left_path)
        right_time, s2 = detect_time(right_path)
        if(s1 & s2):
            if (left_time < right_time):
                tmp_diff = right_time - left_time
            else:
                tmp_diff = left_time - right_time

            if (tmp_diff > timedelta(microseconds=700000)):
                break

            if(tmp_diff < smallest_diff):
                smallest_diff = tmp_diff
                best_left = left_path
                best_right = right_path
            else:
                #os.remove(right_path)
                pass

        right_success, right_image = right_cap.read()
        print('Read a new frame: ', right_success)
        right_count += 1

    print("best time : " + str(smallest_diff))
    df.append({'time': smallest_diff, 'left': best_left, 'right': best_right}, ignore_index=True)

    left_success, left_image = left_cap.read()
    print('Read a new frame: ', left_success)
    left_count += 1


left_cap.release()
right_cap.release()