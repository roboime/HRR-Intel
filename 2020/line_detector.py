import math
import cv2
import numpy as np


def region_of_interest(edges):
    height, width = edges.shape
    poly = np.array([[(0, height), (0, height*(1/2)),
                      (width, height*(1/2)), (width, height)]], np.int32)
    mask = np.zeros_like(edges)
    if len(edges.shape) > 2:
        channel_count = edges.shape[2]
        ignore_mask_color = (255,)*channel_count
    else:
        ignore_mask_color = 255
    cv2.fillPoly(mask, poly, ignore_mask_color)
    cropped_edges = cv2.bitwise_and(mask, edges)
    return cropped_edges


def find_lines(cropped):
    rho = 1
    angle = np.pi/180
    min_threshold = 50
    line_segments = cv2.HoughLinesP(
        cropped,
        rho,
        angle,
        min_threshold,
        np.array([]),
        minLineLength=8,
        maxLineGap=4
    )
    return line_segments


def make_coordinates(image, lines):
    if lines.shape[0] == 0:
        return
    slope, intercept = lines
    y1 = image.shape[0]
    y2 = int(y1*(1/2))
    x1 = int((y1-intercept)/slope)
    x2 = int((y2-intercept)/slope)
    return [x1, y1, x2, y2]


def average_slope_intercept(image, lines):
    left_lines = []
    right_lines = []
    left_x = []
    right_x = []
    if lines is None:
        print("The robot cannot recognize anything!")
        return None

    for i in range(lines.shape[0]):
        x1, y1, x2, y2 = lines[i][0]
        fit = np.polyfit((x1, x2), (y1, y2), 1)
        if fit[0] > 0:
            right_lines.append(fit)
        else:
            left_lines.append(fit)

    if len(left_lines) > 0:
        for j in range(len(left_lines)):
            left_x.append(560/left_lines[j][0] -
                          left_lines[j][1]/left_lines[j][0])

        x_main = min(left_x)
        a = left_x.index(x_main)
        left_average = left_lines[a]
        #left_average = np.average(left_lines, axis=0)
    else:
        left_average = np.array([])
    if len(right_lines) > 0:
        for k in range(len(right_lines)):
            right_x.append(560/right_lines[k][0] -
                           right_lines[k][1]/right_lines[k][0])
        x_main = max(right_x)
        b = right_x.index(x_main)
        right_average = right_lines[b]
        #right_average = np.average(right_lines, axis=0)
    else:
        right_average = np.array([])
    return [make_coordinates(image, left_average), make_coordinates(image, right_average)]


def make_central_line(image, lines):
    if lines[0] is []:
        middle_line = lines[1]
        x1, y1, x2, y2 = middle_line
        fit = np.polyfit((x1, x2), (y1, y2), 1)
        return [make_coordinates(image, fit), fit]
    if lines[1] is []:
        middle_line = lines[0]
        x1, y1, x2, y2 = middle_line
        fit = np.polyfit((x1, x2), (y1, y2), 1)
        return [make_coordinates(image, fit), fit]
    middle_line = np.average(lines, axis=0)
    x1, y1, x2, y2 = middle_line
    fit = np.polyfit((x1, x2), (y1, y2), 1)
    return [make_coordinates(image, fit), fit]


def canny(image):
    blur = cv2.GaussianBlur(image, (5, 5), 0)
    canny = cv2.Canny(blur, 200, 400)
    cv2.imwrite('canny.jpg', canny)
    return canny


def line_detector():
    img = cv2.imread('image.jpg')
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(img_hsv, np.array([0, 0, 39]), np.array([179, 220, 65]))
    edges = canny(mask)
    cropped_edges = region_of_interest(edges)
    cv2.imwrite('ce.jpg', cropped_edges)
    lines = average_slope_intercept(img, find_lines(cropped_edges))
    central_line = make_central_line(img, lines)
    poly_1 = central_line[1]
    poly_2 = [1/poly_1[0], -poly_1[1]/poly_1[0]]
    return poly_2
