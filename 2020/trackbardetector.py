import cv2
import numpy as np
img = cv2.imread('i.jpg')
img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
window_original_name = 'Original'
window_detection_name = 'Threshold'
trackbar_window = 'Trackbar'
low_H = 0
low_S = 0
low_V = 0
high_H = 179
high_S = 255
high_V = 255


def on_low_H_thresh_trackbar(val):
    global low_H
    global high_H
    low_H = val
    low_H = min(high_H-1, low_H)
    cv2.setTrackbarPos('Low H', window_detection_name, low_H)


def on_high_H_thresh_trackbar(val):
    global low_H
    global high_H
    high_H = val
    high_H = max(high_H, low_H+1)
    cv2.setTrackbarPos('high H', window_detection_name, high_H)


def on_low_S_thresh_trackbar(val):
    global low_S
    global high_S
    low_S = val
    low_S = min(high_S-1, low_S)
    cv2.setTrackbarPos('Low S', window_detection_name, low_S)


def on_high_S_thresh_trackbar(val):
    global low_S
    global high_S
    high_S = val
    high_S = max(high_S, low_S+1)
    cv2.setTrackbarPos('High S', window_detection_name, high_S)


def on_low_V_thresh_trackbar(val):
    global low_V
    global high_V
    low_V = val
    low_V = min(high_V-1, low_V)
    cv2.setTrackbarPos('Low V', window_detection_name, low_V)


def on_high_V_thresh_trackbar(val):
    global low_V
    global high_V
    high_V = val
    high_V = max(high_V, low_V+1)
    cv2.setTrackbarPos('High V', window_detection_name, high_V)


cv2.namedWindow(window_original_name)
cv2.namedWindow(window_detection_name)
cv2.namedWindow('Trackbar')

cv2.createTrackbar('Low H', 'Trackbar',
                   low_H, 179, on_low_H_thresh_trackbar)
cv2.createTrackbar('High H', trackbar_window,
                   high_H, 179, on_high_H_thresh_trackbar)
cv2.createTrackbar('Low S', trackbar_window,
                   low_S, 255, on_low_S_thresh_trackbar)
cv2.createTrackbar('High S', trackbar_window,
                   high_S, 255, on_high_S_thresh_trackbar)
cv2.createTrackbar('Low V', trackbar_window,
                   low_V, 255, on_low_V_thresh_trackbar)
cv2.createTrackbar('High V', trackbar_window,
                   high_V, 255, on_high_V_thresh_trackbar)

while True:
    img_thresh = cv2.inRange(
        img_hsv, (low_H, low_S, low_V), (high_H, high_S, high_V))
    result = cv2.bitwise_or(img_hsv, img_hsv, mask=img_thresh)
    cv2.imshow(window_original_name, img)
    """cv2.imshow('HSV', img_hsv)"""
    cv2.imshow(window_detection_name, result)
    key = cv2.waitKey(30)
    if key == ord('q') or key == 27:
        break
