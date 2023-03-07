import pytesseract
from PIL import Image
import cv2

# img = Image.open('Opencv\data\image2.jpg')
img = cv2.imread('Opencv\data\image2.png')
img = cv2.resize(img,(800,800))

txt = pytesseract.image_to_string(img, lang='tha')
# osd = pytesseract.image_to_osd(img, lang='eng')
# dp = pytesseract.image_to_data(img, lang='eng', pandas_config=1)
# box = pytesseract.image_to_boxes(img, lang='tha')
print(txt)

print("type: ", type(txt))
print(txt.splitlines())

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