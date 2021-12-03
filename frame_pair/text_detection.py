from datetime import datetime

import cv2
import pytesseract

def detect_time(image_path):
    pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"

    img = cv2.imread(image_path)

    # Preprocessing the image starts

    # Convert the image to gray scale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Performing OTSU threshold
    ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

    # Specify structure shape and kernel size.
    # Kernel size increases or decreases the area
    # of the rectangle to be detected.
    # A smaller value like (10, 10) will detect
    # each word instead of a sentence.
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))

    # Applying dilation on the threshold image
    dilation = cv2.dilate(thresh1, rect_kernel, iterations=1)

    # Finding contours
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_NONE)
    # Creating a copy of image
    im2 = img.copy()

    # Looping through the identified contours
    # Then rectangular part is cropped and passed on
    # to pytesseract for extracting text from it
    # Extracted text is then written into the text file
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)

        # Drawing a rectangle on copied image
        rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Cropping the text block for giving input to OCR
        cropped = im2[y:y + h, x:x + w]
        # Apply OCR on the cropped image
        text = pytesseract.image_to_string(cropped)

    try:
        good_text = False
        t_time = ""
        for i in text:
            if(i.isnumeric()):
                t_time += i
            elif(i == ":"):
                t_time += i
            elif (i == "."):
                t_time += "."

        datetime_object = datetime.strptime(t_time, '%H:%M:%S.%f')
        good_text = True

    except:
        print(str(text))
        datetime_object = "f"


    #return t_time
    return datetime_object


def total_time(p_time = "", start_time = "20:46:1.1"):
    a = p_time.split(':')
    w = a[2].split('.')

    b = start_time.split(':')
    c = b[2].split('.')

    t_time = int(a[1])*60*1000000 + int(w[0])*1000000 + int(w[1])

    return t_time