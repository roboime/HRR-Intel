import numpy as np
import cv2

img = np.zeros((512,512,3), np.uint8) # imagem preta

cv2.line(img,(0,0),(511,511),(255,0,0),5)
cv2.rectangle(img,(384,0),(510,128),(0,255,0),3)
cv2.circle(img,(447,63), 63, (0,0,255), -1)

font = cv2.FONT_HERSHEY_SIMPLEX
cv2.putText(img,'OpenCV',(10,500), font, 4,(255,255,255),2,cv2.LINE_AA)

while True:
    cv2.imshow("imagem", img)
    k = cv2.waitKey(6)
    if k == ord('s'):
        cv2.imwrite('2.jpg', img)
    if k & 0xff == 27:
        cv2.destroyAllWindows()
        break