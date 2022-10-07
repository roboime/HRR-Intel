import cv2
import sys

img = cv2.imread('img.jpg')

if img is None:
    sys.exit("Could not read the image.")

cv2.imshow("imagem", img)
k = cv2.waitKey(0)
if k == ord('s'):
    cv2.imwrite('1.jpg', img)
cv2.destroyAllWindows()