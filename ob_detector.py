import cv2
import numpy as np


def xy(image):
    img = cv2.imread(image)
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    #cv2.imshow('HSV', img_hsv)
    kernel = np.ones((5, 5), np.uint8)
    rangomax = np.array([20, 255, 255])
    rangomin = np.array([5, 125, 90])

    mask = cv2.inRange(img_hsv, rangomin, rangomax)
    #cv2.imshow('mask', mask)
    opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    #cv2.imshow('opening', opening)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
    #cv2.imshow('closing', closing)
    closing2 = cv2.morphologyEx(closing, cv2.MORPH_CLOSE, kernel)
    #cv2.imshow('closing2', closing2)
    edges = cv2.Canny(closing2, 200, 200)

    contours, hierarchy = cv2.findContours(
        edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_poly = [None]*len(contours)
    boundRect = [None]*len(contours)
    for i, c in enumerate(contours):
        contours_poly[i] = cv2.approxPolyDP(c, 3, True)
        boundRect[i] = cv2.boundingRect(contours_poly[i])
    drawing = np.zeros((edges.shape[0], edges.shape[1], 3), dtype=np.uint8)
    for i in range(len(contours)):
        color = (0, 255, 0)
        if boundRect[i][2] > 250:
            #cv2.drawContours(img, contours_poly, i, color)
            # cv2.rectangle(img, (int(boundRect[i][0]), int(boundRect[i][1])),
            # (int(boundRect[i][0]+boundRect[i][2]), int(boundRect[i][1]+boundRect[i][3])), color, 2)
            #cv2.rectangle(img, (0, 0), (20, 20), color, 2)
            x = int(boundRect[i][0]+boundRect[i][2]/2)
            y = int(boundRect[i][1]+boundRect[i][3]/2)
            print(x, y)
            return x, y
        else:
            pass


xy('images/imagem5.jpeg')
