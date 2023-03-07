import cv2 as cv
import numpy as np
import os

cap = cv.VideoCapture(1)

cap.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 720)
cap.set(cv.CAP_PROP_FPS, 60)

lower_white = np.array([0,0,180])
upper_white = np.array([255,50,255])

# path = "Opencv/data"

# if not os.path.exists(path=path):
#     os.makedirs(path)

while cap.isOpened():

    _, frame = cap.read()
    image = frame.copy()

    blur = cv.GaussianBlur(frame, (5, 5), 0)
    hsv = cv.cvtColor(blur, cv.COLOR_BGR2HSV)
    binary = cv.inRange(hsv, lower_white, upper_white)

    white_pixels = cv.bitwise_and(frame, frame, mask=binary)

    try:
        countour, _ = cv.findContours(binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        area  = [cv.contourArea(cnt) for cnt in countour]
        cnt = countour[area.index(max(area))]
        x, y, w, h = cv.boundingRect(cnt)
        cv.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
        # print("find countour")
    except:
        pass

    cv.imshow('frame', frame)

    if cv.waitKey(1) == ord('q'):
        break

    # if cv.waitKey(1) == ord("s"):
    #     cv.imwrite(f"{path}/dataIMG.png", frame)
    #     print("save")

    if cv.waitKey(1) == ord("c"):
        crop = image[y:y+h, x:x+w]
        break

cv.destroyAllWindows()
cap.release()

cv.imwrite("Opencv/data/cropIMG.png", crop)
cv.imshow('crop', crop)
# cv.inshow('corrected', corrected) 
cv.waitKey(0)
cv.destroyAllWindows()