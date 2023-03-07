import cv2 as cv 
import numpy as np
import pytesseract
import re

cap = cv.VideoCapture(1)
# w = cap.get(cv.CAP_PROP_FRAME_WIDTH)
# h = cap.get(cv.CAP_PROP_FRAME_HEIGHT)
w, h = 1920, 1080

# print("w: ", w, "h: ", h)

gap_x, gap_y = 800,1000
cap.set(cv.CAP_PROP_FRAME_WIDTH, w)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, h)
cap.set(cv.CAP_PROP_FPS, 60)

x1, x2, y1, y2 = int(w/2 - gap_x/2), int(w/2 + gap_x/2), int(h/2 - gap_y/2), int(h/2 + gap_y/2)
# print("x1: ", x1, "x2: ", x2, "y1: ", y1, "y2: ", y2)

while cap.isOpened():

    ret, frame = cap.read()
    image = frame.copy()
    cv.rectangle(frame, (x1,y1), (x2,y2), (0, 0, 255), 3)

    frame = cv.resize(frame, (w//2, h//2))
    cv.imshow('frame', frame)

    if cv.waitKey(1) == ord('q'):
        slip_img = np.zeros((480, 640, 3), np.uint8)
        is_slip = False
        break

    elif cv.waitKey(1) == ord("c"):
        cv.destroyAllWindows()
        slip_img = image[y1:y2, x1:x2]
        is_slip = True
        break
    
cap.release()
cv.destroyAllWindows()

resize_size = (int(gap_x*0.8), int(gap_y*0.8))
# slip = cv.resize(slip_img.copy(), resize_size)
# cv.imshow("Slip", cv.resize(slip_img.copy(), resize_size))
# cv.waitKey(3000)
# print("Slip Size: ", slip_img.shape)
# cv.destroyAllWindows()

if is_slip:

    data_dict = {"Name_send" : None,
                 "Name_receive" : None,
                 "Amount" : None,
                 "Date" : None,
                 "Time" : None,}
    # name_prefix_TH = ["นาย", "นาง", "นางสาว", "น.ส."]
    # name_prefix_EN = ["Mr.", "Mrs.", "Ms."]
    name_prefix = ["นาย", "นาง", "นางสาว", "น.ส.", "Mr.", "Mrs.", "Ms."]
    amount_prefix = ["บาท", "THB"]
    # name_prefix = name_prefix_TH + name_prefix_EN
    month_TH =  ["ม.ค.", "ก.พ.", "มี.ค.", "เม.ย.", "พ.ค.", "มิ.ย.", "ก.ค.", "ส.ค.", "ก.ย.", "ต.ค.", "พ.ย.", "ธ.ค."]
    month_EN =  ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]

    # textExtract = []1
    h = slip_img.shape[0]
  
    # cv.imshow("Slip", slip_img)
    # cv.waitKey(1000)

    print("----- Starting to read text -----")
    text_TH = pytesseract.image_to_string(slip_img, lang='tha')
    text_EN = pytesseract.image_to_string(slip_img, lang='eng')

    if len(text_TH) == 0 and len(text_EN) == 0:
        # print("*** No text detected ***")
        # box = pytesseract.image_to_boxes(slip_img, lang='tha')
        text = "No text detected"

    elif len(text_EN) == 0:
        # box = pytesseract.image_to_boxes(slip_img, lang='tha')
        text = text_TH
    
    elif len(text_TH) == 0:
        # box = pytesseract.image_to_boxes(slip_img, lang='eng')
        text = text_EN
    
    else:
        for pref in name_prefix:
            if pref.upper() in text_TH.upper():
                text = text_TH
                break
            elif pref.upper() in text_EN.upper():
                text = text_EN
                break

    print("----- Text Are -----")
    # print("THAI\n",text_TH)
    # print("ENG\n",text_EN)
    print(text)

    # for b in box.splitlines():
    #         b = b.split(" ")
    #         cv.rectangle(slip_img, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 0, 255), 1)
                # cv2.putText(img, b[0], (int(b[1]), h - int(b[2])), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255), 1)

    slip_img = cv.resize(slip_img, resize_size)
    cv.imshow("Slip Detect", slip_img)
    cv.waitKey(3000)

cv.destroyAllWindows()

text_list = text.splitlines()
print(text_list)

loop_name = 0
loop_amount = 0

for var in text_list:
    if "-" in var:
        name = text_list[text_list.index(var)-1]
        if loop_name == 0:
            data_dict["Name_send"] = name
            loop_name += 1
            continue
        else:
            data_dict["Name_receive"] = name
            continue

    split = var.split(" ")
    for i in split:
        if i in name_prefix: # Detect Name:
            name = " ".join(split[split.index(i):])
            if loop_name==0:
                data_dict["Name_send"] = name
                loop_name += 1
            else:
                data_dict["Name_receive"] = name
        
        elif i.upper() in month_TH: # Detect Date & Time -- TH:
            date_time = split
            print("date_time", date_time)
            month_index = date_time.index(i)
            month = month_EN[month_TH.index(i)]
            date = [date_time[month_index-1],date_time[month_index+1]]
            time = date_time[month_index+2]
            data_dict["Date"] = f"{date[0]}-{month}-{date[1]}"
            data_dict["Time"] = time

        elif i.upper() in month_EN: # Detect Date & Time -- EN:
            date_time = split
            print("date_time", date_time)
            month_index = date_time.index(i)
            month = i.upper()
            date = [date_time[month_index-1],date_time[month_index+1]]
            time = date_time[month_index+2]
            data_dict["Date"] = f"{date[0]}-{month}-{date[1]}"
            data_dict["Time"] = time
        # print("var", var)
        # print("split", split)

        elif i in amount_prefix: # Detect Amount:
            if loop_amount==0:
                amount = "".join(v for v in var if v.isdigit() or v==".")
                data_dict["Amount"] = float(amount)
                loop_amount += 1
            else:
                continue

print(data_dict)
