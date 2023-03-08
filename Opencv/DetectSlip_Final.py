import cv2 as cv 
import numpy as np
import pytesseract
import subprocess
import tkinter as tk
from tkinter import messagebox

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
    cv.rectangle(frame, (x1,y1), (x2,y2), (200, 0, 100), 3, cv.LINE_AA)
    cv.putText(frame, "Put your slip in the box", (x1+15, y1+40), cv.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 2, cv.LINE_AA)

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

    slip_img_show = cv.resize(slip_img.copy(), resize_size)
    cv.imshow("Slip Detect", slip_img_show)
    cv.waitKey(3000)
    cv.destroyAllWindows()

    data_dict = {"Name_send" : None,
                 "Name_receive" : None,
                 "Amount" : None,
                 "Date" : None,
                 "Time" : None,}

    name_prefix = ["นาย", "นาง", "นางสาว", "น.ส.","บริษัท", "บจก.", "บจก", "หจก", "Mr.", "Mrs.", "Ms.", "Co.", "Ltd.", "Inc."]
    amount_prefix = ["บาท", "THB", "จํานวนเงิน"]

    month_TH =  ["ม ค ", "ก พ ", "มี ค ", "เม ย ", "พ ค ", "มิ ย ", "ก ค ", "ส ค ", "ก ย ", "ต ค ", "พ ย ", "ธ ค "]
    month_EN =  ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]

    h = slip_img.shape[0]

    print("----- Starting to read text -----")
    text_TH = pytesseract.image_to_string(slip_img, lang='tha')
    text_EN = pytesseract.image_to_string(slip_img, lang='eng')

    if len(text_TH) == 0 and len(text_EN) == 0:
        # print("*** No text detected ***")
        # box = pytesseract.image_to_boxes(slip_img, lang='tha')
        text = "No text detected"
    
    else:
        for pref in name_prefix:
            if pref.upper() in text_TH.upper(): #Check language --TH and detect name
                text = text_TH
                break
            elif pref.upper() in text_EN.upper(): #Check language --EN and detect name
                text = text_EN
                break
            else:
                text = "No name detected, Not a slip!"

    name_raw = [name for name in text.splitlines() if len(name.split(" ")) >= 2 and len(name.split(" ")) <= 3]
    name = []

    for var in name_raw: #Detect name
        if all(item.isalpha() for item in var.split(" ")):
            name.append(var)
            continue
        for pref in name_prefix:
            if pref.upper() in var.upper():
                indx = var.upper().index(pref.upper())
                name.append(var[indx::])
                break

    # name = [var for var in name for pref in name_prefix if pref.upper() in var.upper() or all(item.isalpha() for item in var.split(" "))]
    
    print("----- Text Are -----")
    # print("THAI\n",text_TH)
    # print("ENG\n",text_EN)
    print(text)
    print("----- Name Are -----")
    print(name, end = "\n\n")


    if len(name) == 2:
        data_dict["Name_send"] = name[0]
        data_dict["Name_receive"] = name[1]
    # print(name)
    # for b in box.splitlines():
    #         b = b.split(" ")
    #         cv.rectangle(slip_img, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 0, 255), 1)
                # cv2.putText(img, b[0], (int(b[1]), h - int(b[2])), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255), 1)


text_list = [i.replace("  ","") for i in text.splitlines() if len(i) > 0]

print("----- Text List Are -----")
print(text_list, end = "\n\n")

loop_name = 0
loop_amount = 0

for var in text_list:

    split = var.split(" ")

    for i in split:

        if i.upper().replace("."," ").replace(","," ") in month_TH: # Detect Date & Time -- TH:
            date_time = [i for i in split if len(i)>0]
            # print("date_time", date_time)
            index = date_time.index(i)
            month = month_EN[month_TH.index(i.replace("."," ").replace(","," "))]  
            date = [date_time[index-1],date_time[index+1]]
            time = [i for i in date_time if ":" in i and i != "วันที่:"][0]
            data_dict["Date"] = f"{date[0]}-{month}-{date[1]}"
            data_dict["Time"] = time

        elif i.upper() in month_EN: # Detect Date & Time -- EN:
            date_time = [i for i in split if len(i)>0]
            # print("date_time", date_time)
            index = date_time.index(i)
            month = i.upper()
            date = [date_time[index-1],date_time[index+1]]
            time = [i for i in date_time if ":" in i and i != "วันที่:"][0]
            data_dict["Date"] = f"{date[0]}-{month}-{date[1]}"
            data_dict["Time"] = time
        # print("var", var)
        # print("split", split)

        elif i in amount_prefix: # Detect Amount:
            if loop_amount==0:
                amount = "".join(v for v in var if v.isdigit())
                # print("amount", var)
                amount = float(f"{amount[:-2]}.{amount[-2:]}")
                data_dict["Amount"] = amount
                loop_amount += 1
            else:
                continue

print("----- Data Dictionary From Slip -----")
print(data_dict)

root = tk.Tk()
root.withdraw()

if None in data_dict.values():
    # print("!!!!!! Cannot Receive All Data, Try Again !!!!!!")
    result = messagebox.askretrycancel("Error", "Cannot Receive All Data, Do you want to Try Again")
    # print("result", result)
    if result:
        py_path = "G:\git\programming4\projectFinal\Opencv\crop_camera.py"
        subprocess.run(["python", py_path])

    else:
        messagebox.showinfo("Success", "Done")

else:
    messagebox.showinfo("Success", "Receive All Data")

root.destroy()