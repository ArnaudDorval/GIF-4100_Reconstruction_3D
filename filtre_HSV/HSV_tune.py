import cv2
import numpy as np


image_name = "./image/left_frame8443.jpg"
frame = cv2.imread(image_name)

hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
lower_red = np.array([7, 0, 95])
upper_red = np.array([170, 255, 255])
mask = cv2.inRange(hsv, lower_red, upper_red)
res = cv2.bitwise_and(frame, frame, mask = mask)


cv2.imshow('frame', frame)
cv2.imshow('mask', mask)
cv2.imshow('res', res)
cv2.waitKey(0)
cv2.destroyAllWindows()
print("ok")

#(hMin = 7 , sMin = 0, vMin = 95), (hMax = 170 , sMax = 255, vMax = 255)




#dark_red = np.uint8([[[12, 22, 121]]])
#dark_red = cv2.cvtColor(dark_red, cv2.COLOR_BGR2HSV)