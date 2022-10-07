import cv2
import sys
from cv2 import ROTATE_180
import numpy as np

img = cv2.imread('img.jpg')

if img is None:
    sys.exit("Could not read the image.")

print(img.shape)
print(img.size)
print(img.dtype)

roi = img[0:img.shape[0]//2, 0:img.shape[1]//2]
rotated = cv2.rotate(roi, ROTATE_180)
resized = cv2.resize(img, (roi.shape[1], roi.shape[0]))
up = cv2.hconcat([roi,rotated])
down = cv2.hconcat([resized,resized])
res = cv2.vconcat([up, down])


while True:
    cv2.imshow("image", res)
    k = cv2.waitKey(6)
    if k == ord('s'):
        cv2.imwrite('3.jpg', res)
    if k & 0xff == 27:
        cv2.destroyAllWindows()
        break