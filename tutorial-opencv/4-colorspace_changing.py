import cv2
import sys
import numpy as np

img = cv2.imread('img.jpg')

if img is None:
    sys.exit("Could not read the image.")

img = cv2.resize(img, (img.shape[1]//2, img.shape[0]//2))
img = cv2.rotate(img, cv2.ROTATE_180)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
print(gray.shape)
print(hsv.shape)

while True:
    cv2.imshow("imagem", gray)
    k = cv2.waitKey(6)
    if k == ord('s'):
        cv2.imwrite('4_gray.jpg', img)
    if k & 0xff == 27:
        cv2.destroyAllWindows()
        break
while True:
    cv2.imshow("imagem", hsv)
    k = cv2.waitKey(6)
    if k == ord('s'):
        cv2.imwrite('4_hsv.jpg', img)
    if k & 0xff == 27:
        cv2.destroyAllWindows()
        break