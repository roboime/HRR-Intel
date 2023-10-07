import numpy as np
import cv2
import sys

img = cv2.imread('img.jpg')
if img is None:
    sys.exit("Could not read the image.")

img_HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(img_HSV, (1, 75, 105), (16, 211, 233))

kernel = np.ones((5,5),np.uint8)
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

contours, _ = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
for c in contours:
    print(c)
    x,y,w,h = cv2.boundingRect(c)
    cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),3)
cv2.drawContours(img,contours,-1,(0,0,255),3)
cv2.imshow('output',img)
while True:
    k = cv2.waitKey(6)
    if k == ord('s'):
        cv2.imwrite('6.jpg', img)
    if k & 0xff == 27:
        break