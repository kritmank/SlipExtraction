import cv2 as cv

cap = cv.VideoCapture(2)

if cap.isOpened():
    print("Camera is opened")

else:
    print("Camera is not opened")

while cap.isOpened():
    ret, frame = cap.read()
    cv.imshow('frame', frame)

    if cv.waitKey(1) == ord('q'):
        break