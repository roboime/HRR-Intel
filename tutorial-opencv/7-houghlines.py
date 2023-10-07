import cv2
import numpy as np

th1 = 130
th2 = 50
aperturesize = 3
th3 = 100
minLineLength = 100
maxLineGap = 10

def on_th1(val):
    global th1
    th1 = val
    cv2.setTrackbarPos("threshol1", "fon", th1)
def on_th2(val):
    global th2
    th2 = val
    cv2.setTrackbarPos("threshol2", "fon", th2)
def on_th3(val):
    global th3
    th3 = val
    cv2.setTrackbarPos("threshol3", "fon", th3)
def on_aperturesize(val):
    global aperturesize
    if val & 1 and val >=3:
        aperturesize = val
    cv2.setTrackbarPos("aperturesize", "fon", aperturesize)
def on_minLineLength(val):
    global minLineLength
    minLineLength = val
    cv2.setTrackbarPos("minLineLength", "fon", minLineLength)
def on_maxLineGap(val):
    global maxLineGap
    maxLineGap = val
    cv2.setTrackbarPos("maxLineGap", "fon", maxLineGap)

cv2.namedWindow("fon")
cv2.createTrackbar("th1", "fon" , th1, 500, on_th1)
cv2.createTrackbar("th2", "fon" , th2, 500, on_th2)
cv2.createTrackbar("aperturesize", "fon" , aperturesize, 7, on_aperturesize)
cv2.createTrackbar("th3", "fon" , th3, 500, on_th3)
cv2.createTrackbar("minLineLength", "fon" , minLineLength, 500, on_minLineLength)
cv2.createTrackbar("maxLineGap", "fon" , maxLineGap, 500, on_maxLineGap)

while True:
    img = cv2.imread('img.jpg')

    img_HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(img_HSV, (1, 75, 105), (16, 211, 233))

    kernel = np.ones((5,5),np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    edges = cv2.Canny(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY),th1,th2, apertureSize=aperturesize)
    lines = cv2.HoughLinesP(edges,1,np.pi/180, threshold=th3,minLineLength=minLineLength,maxLineGap=maxLineGap)
    if lines is not None:
        for line in lines:
            x1,y1,x2,y2 = line[0]
            cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
            #print (line)
    cv2.imshow('Hough lines P', img)
    cv2.imshow('canny', edges)
    
    k = cv2.waitKey(6)
    if k == ord('s'):
        cv2.imwrite('7.jpg', img)
    if k & 0xff == 27:
        break