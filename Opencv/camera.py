import cv2 as cv 
import numpy as np
import easyocr
import time

cap = cv.VideoCapture(0)

is_slip = False

while cap.isOpened():
    ret, frame = cap.read()
    cv.imshow('frame', frame)

    if cv.waitKey(1) == ord('q'):
        break

    elif cv.waitKey(1) == ord("c"):
        slip_img = frame
        is_slip = True
        break

cap.release()
cv.destroyAllWindows()


if is_slip:

    textExtract = []

    cv.imshow("Slip", slip_img)
    cv.waitKey(1000)
    # time.sleep(1)
    cv.destroyAllWindows()

    print("----- Starting to read text -----")
    reader = easyocr.Reader(['en',"th"], gpu=False)
    result = reader.readtext(slip_img)

    if len(result) == 0:
        print("*** No text detected ***")

    else:
        for detect in result:
            TopLeft=tuple([int(val) for val in detect[0][0]])
            BottomLeft=tuple([int(val) for val in detect[0][2]])
            text=detect[1]
            font=cv.FONT_HERSHEY_COMPLEX
            cv.rectangle(slip_img,TopLeft,BottomLeft,(255,0,255),3)
            cv.putText(slip_img,text,TopLeft,font,.5,(2,48,71),2,cv.LINE_AA)
            textExtract.append(text)
            print(text)

    cv.imshow("Slip", slip_img)
    cv.waitKey(0)

else:
    black = np.zeros((480, 640, 3), np.uint8)
    cv.imshow("Slip", black)
    cv.waitKey(0)

cv.destroyAllWindows()