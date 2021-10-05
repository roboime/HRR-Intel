#!/usr/bin/env python
# coding: utf-8



import numpy as np
import cv2


def flinha(img, n):
    image=cv2.imread(img)
    hls = cv2.cvtColor(image, cv2.COLOR_BGR2HLS)
    lower=np.array([0,0,0])
    upper=np.array([255,70,255])

    blackmask=cv2.inRange(hls, lower,upper)
    kernel=np.ones((7,7),np.uint8)
    opening=cv2.morphologyEx(blackmask, cv2.MORPH_OPEN,kernel)
    
    edges=cv2.Canny(opening,150,240,apertureSize=3)

    cv2.imwrite('edges'+str(n+1)+".jpeg",edges)
    cv2.imwrite('mask'+str(n+1)+".jpeg",blackmask)
    minLineLength=100
    lines = cv2.HoughLinesP(edges,rho=1,theta=np.pi/180, threshold=100,lines=np.array([]), minLineLength=minLineLength,maxLineGap=20)

    a,b,c = lines.shape

    for i in range(a):

        ang=(180/np.pi)*np.arctan((lines[i][0][3]-lines[i][0][1])/(lines[i][0][2]-lines[i][0][0]))
        print(ang)
        if abs(ang)>20 and abs(ang)<80:
            cv2.line(image, (lines[i][0][0], lines[i][0][1]), (lines[i][0][2], lines[i][0][3]), (0, 0, 255), 3, cv2.LINE_AA)
        cv2.imwrite('teste'+str(n+1)+".jpeg",image)











