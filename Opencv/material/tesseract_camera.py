import cv2 as cv 
import numpy as np
import pytesseract
import time

cap = cv.VideoCapture(0)

cap.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 720)
cap.set(cv.CAP_PROP_FPS, 60)

lower_white = np.array([0,0,180])
upper_white = np.array([255,50,255])

x1, y1, x2, y2 = 400, 20, 880, 700

while cap.isOpened():

    ret, frame = cap.read()
    image = frame.copy()
    cv.rectangle(frame, (x1,y1), (x2,y2), (0, 0, 255), 3)
    blur = cv.GaussianBlur(frame, (5, 5), 0)
    hsv = cv.cvtColor(blur, cv.COLOR_BGR2HSV)
    binary = cv.inRange(hsv, lower_white, upper_white)

    try:
        countour, _ = cv.findContours(binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        area  = [cv.contourArea(cnt) for cnt in countour]
        cnt = countour[area.index(max(area))]
        # print("area", max(area))
        x, y, w, h = cv.boundingRect(cnt)
        # cv.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 1)
        # print("find countour")

    except:
        pass

    cv.imshow('frame', frame)
    cv.imshow('binary', binary)

    if cv.waitKey(1) == ord('q'):
        black = np.zeros((480, 640, 3), np.uint8)
        cv.imshow("Slip", black)
        cv.waitKey(0)
        is_slip = False
        break

    elif cv.waitKey(1) == ord("c"):
        cv.destroyAllWindows()
        slip_img = image[y:y+h, x:x+w]
        cv.imshow("Slip", slip_img)
        cv.waitKey(5000)
        is_slip = True
        break
    
cap.release()
cv.destroyAllWindows()

if is_slip:

    # textExtract = []1
    h = slip_img.shape[0]
  
    # cv.imshow("Slip", slip_img)
    # cv.waitKey(1000)

    print("----- Starting to read text -----")
    text_TH = pytesseract.image_to_string(slip_img, lang='tha')
    text_EN = pytesseract.image_to_string(slip_img, lang='eng')

    if len(text_TH) == 0 and len(text_EN) == 0:
        print("*** No text detected ***")
        # text = "No text detected"

    elif len(text_TH) == 0:
        box = pytesseract.image_to_boxes(slip_img, lang='eng')
        # text = text_EN
    
    elif len(text_EN) == 0:
        box = pytesseract.image_to_boxes(slip_img, lang='tha')
        # text = text_TH

    print("----- Text Are -----")
    print("THAI\n",text_TH)
    print("ENG\n",text_EN)

    if len(text) == 0:
        print("*** No text detected ***")

    else:
        for b in box.splitlines():
            b = b.split(" ")
            cv.rectangle(slip_img, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 0, 255), 1)
                # cv2.putText(img, b[0], (int(b[1]), h - int(b[2])), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255), 1)

    cv.imshow("Slip Detect", slip_img)
    cv.waitKey(0)

else:
    black = np.zeros((480, 640, 3), np.uint8)
    cv.imshow("Slip", black)
    cv.waitKey(0)

cv.destroyAllWindows()

# h = img.shape[0]
# # print("h: ", h, "w: ", w, "c: ", c)

# # print(b)
# # print(b[0].split(" "))

# for b in box.splitlines():
#     b = b.split(" ")
#     cv2.rectangle(img, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 0, 255), 1)
#     # cv2.putText(img, b[0], (int(b[1]), h - int(b[2])), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255), 1)

# cv2.imshow('img', img)
# cv2.waitKey(0)

# cv2.imshow('img', img)
# cv2.waitKey(0)