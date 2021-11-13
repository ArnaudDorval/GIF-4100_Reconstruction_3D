import numpy as np
import cv2

cap_0 = cv2.VideoCapture(1)
cap_1 = cv2.VideoCapture(2)

while (True):
    # Capture frame-by-frame
    ret0, frame0 = cap_0.read()
    ret1, frame1 = cap_1.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame0, cv2.COLOR_BGR2GRAY)

    if (ret0):
        cv2.imshow('cam 0 ', frame0)
    if (ret1):
        cv2.imshow('cam 1 ', frame1)

    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap_0.release()
cap_1.release()
cv2.destroyAllWindows()