import cv2 as cv
import numpy as np

lower_white = np.array([0,0,180])
upper_white = np.array([255,50,255])

frame = cv.imread("Opencv/data/dataIMG.png")

blur = cv.GaussianBlur(frame, (5, 5), 0)
hsv = cv.cvtColor(blur, cv.COLOR_BGR2HSV)
binary = cv.inRange(hsv, lower_white, upper_white)
white_pixels = cv.bitwise_and(frame, frame, mask=binary)

countours, _ = cv.findContours(binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
# cv.drawContours(frame, countours, -1, (255, 0, 0), -1)

old_area = 0

# for cnt in countours:
#     area = cv.contourArea(cnt)
#     if area<20000:
#         continue
#     # print(cnt)
#     print("area : ", area)
#     x, y, w, h = cv.boundingRect(cnt)
#     cv.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
#     cv.putText(frame, str(area), (x, y), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
# # cnt = countours[3]

area = [cv.contourArea(cnt) for cnt in countours]
print("Max area : ",area.index(max(area)))

cnt = countours[area.index(max(area))]
x, y, w, h = cv.boundingRect(cnt)
cv.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
cv.putText(frame, str(area), (x, y), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

crop_img = frame[y:y+h, x:x+w]

# print("area : ", area)
cv.imshow('binary', binary)
cv.imshow('frame', frame)
cv.imshow('white', white_pixels)
cv.imshow('crop', crop_img)
cv.waitKey(0)