import cv2
import numpy as np

# Define RGB color
blue = np.uint8([[[220,220,220]]])

# Convert to HSV color

hsv_blue = cv2.cvtColor(blue, cv2.COLOR_RGB2HSV)
hsv_blue = np.uint8([[[0,0,255]]])


hsv = cv2.cvtColor(hsv_blue,cv2.COLOR_HSV2BGR)
# hsv = np.uint8([[[0,100,100]]])


img = np.zeros((512, 512, 3), np.uint8)
img[:] = hsv

# Display the image
cv2.imshow('Blue Color', img)
cv2.waitKey(0)


# Print HSV values
print(hsv)
cv2.destroyAllWindows()