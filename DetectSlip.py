import cv2 as cv 
import numpy as np
import tkinter as tk
import pandas as pd
from tkinter import messagebox
from PIL import ImageTk, Image
import pytesseract, subprocess, sys, os

dir_path = os.path.dirname(os.path.abspath(__file__))
py_path = os.path.join(dir_path, "DetectSlip.py")

camera_index = 0
cap = cv.VideoCapture(camera_index)

try:
    calibrate = sys.argv[1]
    camera_index = int(sys.argv[2])

except:
    calibrate = False

if not calibrate:

    root = tk.Tk()
    root.title("Select Camera")
    loop = True


    def increase():
        global camera_index, cap
        cap.release()
        camera_index += 1
        if cv.VideoCapture(camera_index).isOpened():
            cap = cv.VideoCapture(camera_index)
        else:
            camera_index -= 1
            cap = cv.VideoCapture(camera_index)
        # print("camera index", camera_index)
        return None

    def decrease():
        global camera_index, cap
        cap.release()
        camera_index -= 1
        if camera_index < 0:
            camera_index = 0
        cap = cv.VideoCapture(camera_index)
        # print("camera index", camera_index)
        return None

    def ok():
        global loop
        loop = False
        root.destroy()
        return None

    def capture():

        label_cam.config(text=f"Camera Index: {camera_index}")
        ret, frame = cap.read()
        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        image = Image.fromarray(frame)
        tk_image = ImageTk.PhotoImage(image)
        label_img.config(image=tk_image)
        label_img.image = tk_image

        if loop:
            root.after(10, capture)

    tk.Label(root, text="Select Your camera...").pack(side = "top", fill = "both", expand = True, padx = 100, pady = 10)
    label_cam = tk.Label(root)
    label_cam.pack(side = "top", fill = "both", expand = True, padx = 100, pady = 10)
    label_img = tk.Label(root)
    label_img.pack(side = "top", fill = "both", expand = True, padx = 100, pady = 20)
    buttonFrm = tk.Frame(root)
    tk.Button(buttonFrm, text="<<", command=decrease).pack(side="left", padx=10, pady=10)
    tk.Button(buttonFrm, text="OK", command=ok).pack(side="right", padx=10, pady=10)
    tk.Button(buttonFrm, text=">>", command=increase).pack(side="right", padx=10, pady=10)
    buttonFrm.pack(side="bottom", fill="both", expand=True, padx=10, pady=10)

    capture()

    root.mainloop()

root = tk.Tk()
root.withdraw()

cap = cv.VideoCapture(camera_index)
# w = cap.get(cv.CAP_PROP_FRAME_WIDTH)
# h = cap.get(cv.CAP_PROP_FRAME_HEIGHT)
w, h = 1920, 1080

# print("w: ", w, "h: ", h) 

gap_x, gap_y = 800,1000
cap.set(cv.CAP_PROP_FRAME_WIDTH, w)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, h)
cap.set(cv.CAP_PROP_FPS, 60)

x1, x2, y1, y2 = int(w/2 - gap_x/2), int(w/2 + gap_x/2), int(h/2 - gap_y/2), int(h/2 + gap_y/2)
resize_size = (int(gap_x*0.8), int(gap_y*0.8))
# print("x1: ", x1, "x2: ", x2, "y1: ", y1, "y2: ", y2)


def rerunprogram():
    result = messagebox.askretrycancel("Error", "Cannot Receive All Data, Do you want to Try Again")
    # print("result", result)
    if result:
        subprocess.run(["python", py_path, "True", str(camera_index)])
    else:
        messagebox.showinfo("Error", "Please Try Again Later...")
        sys.exit()

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
        cv.imshow("Slip", cv.resize(slip_img, resize_size))
        cv.waitKey(1500)
        result = messagebox.askyesno("Confirm", "Confirm your slip picture.")
        if result:
            is_slip = True
            break
        else:
            cv.destroyAllWindows()
    
cap.release()
cv.destroyAllWindows()

if not is_slip:
    rerunprogram()

# ----------------------- Preprocessing --------------------------------
text_TH = pytesseract.image_to_string(slip_img, lang = 'tha').replace("@","").replace("&","").replace("®","")
text = pytesseract.image_to_string(slip_img, lang='eng+tha').replace("@","").replace("&","").replace("®","")
text_nospace = "".join([v for v in text.split(" ")]).replace("@","").replace("&","").replace("®","")

if len(text_TH) == 0 and len(text) == 0:
    rerunprogram()

data_dict = {"Name_send" : None,
             "Name_receive" : None,
             "Amount" : None,
             "Date" : None,
             "Time" : None,}

name_prefixTH = ["นาย", "นาง", "นางสาว", "น.ส.","บริษัท", "บจก.", "บจก", "หจก", "ทรูมันนี่"]
name_prefixEN = ["Mr.", "Mrs.", "Ms.", "Co.", "Ltd.", "Inc.", "Truemoney"]
name_prefix = name_prefixTH + name_prefixEN

amount_prefix = ["บาท", "THB", "จํานวนเงิน"]

month_TH =  ["ม.ค.", "ก.พ.", "มี.ค.", "เม.ย.", "พ.ค.", "มิ.ย.", "ก.ค.", "ส.ค.", "ก.ย.", "ต.ค.", "พ.ย.", "ธ.ค."]
month_EN =  ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
month_prefix = month_EN + month_TH

text_TH_list = [c for c in text_TH.splitlines() if c != ""]
text_list = [c for c in text.splitlines() if c != ""]
text_nospace_list = [c for c in text_nospace.splitlines() if c != ""]

loop_name = True
loop_month = True

name, amount_list = [], []

# --------------------------- Pre-Detect Month-Date ---------------------------
for var in text_TH_list:
    for indx, pref in enumerate(month_TH):
        if not loop_month:
            break
        if pref in var:
            month = pref
            date_time = var.replace("วันที่:","").replace(month,"")
            date_time = "".join([v for v in date_time if v.isdigit() or v == ":"])
            try:
                indx_colon = date_time.index(":")
            except:
                rerunprogram()

            date = date_time[:indx_colon-2]
            time = date_time[indx_colon-2::]
            date = f"{date[:2]}-{month_EN[indx]}-{date[2::]}"
            loop_month = False
            break
    for indx, pref in enumerate(name_prefixTH):
        if not loop_name:
            break
        if pref in var:
            indx_pref = var.index(pref)
            text_name = var[indx_pref::]
            if len(text_name.split(" ")) >= 2 and len(text_name.split(" ")) <= 3:
                name.append((text_name, indx))
                if len(name)>=2:
                    loop_name = False   

# --------------------------- Detect Algorithm ---------------------------
for indx, var in enumerate(text_nospace_list):

#  Detect Name Part
    if loop_name:
        if var.isalpha():
            text_name = text_list[indx]
            text_name_list = [i for i in text_name.split(" ") if i != ""]
            if len(text_name_list) >= 2 and len(text_name_list) <= 3 and all(items[0].isupper() for items in text_name_list):
                name.append((text_name, indx))

        for pref in name_prefixEN:
            if pref.upper() in var.upper():
                indx_pref = var.upper().index(pref.upper())
                text_name = text_list[indx][indx_pref::]
                if len(text_name.split(" ")) >= 2 and len(text_name.split(" ")) <= 3:
                    name.append((text_name, indx))
        if len(name)>=2:
            loop_name = False       

# Detect Amount Part
    for pref in amount_prefix:

        if pref.upper() in var.upper():
            amount = "".join(i for i in var if i.isdigit() or i==".")
            try:
                indx_dot = amount.index(".")
            except:
                rerunprogram()
            amount = amount[:indx_dot]+amount[indx_dot::]
            amount = float(amount)
            if amount!=0:
                amount_list.append(amount)

# Detect Date & Time Part
    if loop_month:
        for indx_dt, pref in enumerate(month_EN):
            if pref.upper() in var.upper():
                month = pref
                date_time = "".join([c for c in var if c.isdigit() or c == ":"])
                indx_colon = date_time.index(":")
                date = date_time[:indx_colon-2]
                date = f"{date[:2]}-{month}-{date[2::]}"
                time = date_time[indx_colon-2::]

name = sorted(name, key = lambda x: x[1])

try:
    print("textTH", text_TH_list)
    print("text", text_list)
    print("name", name)
    print("amount", amount_list)
    print("date", date)
    print("time", time)
    data_dict["Name_send"] = [name[0][0]]
    data_dict["Name_receive"] = [name[1][0]]
    data_dict["Amount"] = [amount_list[0]]
    data_dict["Date"] = [date]
    data_dict["Time"] = [time]

except:
    rerunprogram()

if None in data_dict.values():
    result = messagebox.askretrycancel("Error", "Cannot Receive All Data, Do you want to Try Again")
    if result:
        subprocess.run(["python", py_path, "True", str(camera_index)])

    else:
        messagebox.showinfo("Success", "Done!")

else:
    message = f"""Receive All Data!

    Name Send: {data_dict["Name_send"][0]}
    Name Receive: {data_dict["Name_receive"][0]}
    Amount: {data_dict["Amount"][0]}
    Date: {data_dict["Date"][0]}
    Time: {data_dict["Time"][0]}

    Save & Scan more. --> Yes
    Save & Not scan.  --> No
    Cancel this data. --> Cancel
    """
    result = messagebox.askyesnocancel("Success", message)
    if result == None:
        result_2 = messagebox.askretrycancel("Retry", "Do you want to try again, or Cancel this data?")
        if result_2:
            subprocess.run(["python", py_path, "True", str(camera_index)])
            sys.exit()
        else:
            messagebox.showinfo("Success", "Done!")
            sys.exit()
    elif result:
        rerun = True
    else:
        rerun = False
        messagebox.showinfo("Success", "Done!")

root.destroy()

dir_datapath = os.path.join(dir_path, "data")
datapath = os.path.join(dir_datapath, "data.csv")

os.makedirs(dir_datapath,exist_ok=True)

try:
    data = pd.read_csv(datapath)
    data = data.to_dict("list")
    for i in range(len(data_dict["Amount"])):
        data["Name_send"].append(data_dict["Name_send"][i])
        data["Name_receive"].append(data_dict["Name_receive"][i])
        data["Amount"][i] = float(data_dict["Amount"][i])
        data["Amount"].append(data_dict["Amount"][i])
        data["Date"].append(data_dict["Date"][i])
        data["Time"].append(data_dict["Time"][i])
        data_to_csv = pd.DataFrame(data)
except:
    data_to_csv = pd.DataFrame(data_dict)

finally:
    data_to_csv.to_csv(datapath, index=False)

if rerun:
    subprocess.run(["python", py_path, "True", str(camera_index)])