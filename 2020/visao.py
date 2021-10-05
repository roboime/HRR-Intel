import math

import cv2
import numpy as np

img = cv2.imread('teste.png')

#Identifica as bordas
def canny(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    canny = cv2.Canny(blur, 200,400)
    return canny

def steering_correction(central_line):
    delta = 90-abs(math.atan(central_line[0])*(180/np.pi))
    if central_line[0] < 0:
        print("Turn", delta, "degrees left" )
    else:
        print("Turn", delta, "degrees right")
        
def show_img(image, central_line):
    cv2.imshow("teste", image)
    steering_correction(central_line)

def region_of_interest(edges):
    height, width = edges.shape
    poly = np.array([[(0,height), (0,height*(1/2)), (width, height*(1/2)), (width, height)]], np.int32)
    mask = np.zeros_like(edges)
    cv2.fillPoly(mask, poly, 255)
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
    return [x1,y1,x2,y2] 

def average_slope_intercept(image, lines):
    
    left_lines = []
    right_lines = []
    
    if lines is None:
        print("The robot cannot recognize anything!")
        return None
    
    for i in range(lines.shape[0]):
        x1,y1,x2,y2 = lines[i][0]
        fit = np.polyfit((x1,x2),(y1,y2), 1)
        if fit[0]>0:
            right_lines.append(fit)
        else:
            left_lines.append(fit)
            
    if len(left_lines)>0:       
        left_average = np.average(left_lines, axis = 0)
    else:
        left_average = np.array([])
    if len(right_lines)>0:
        right_average = np.average(right_lines, axis = 0)
    else:
        right_average = np.array([])
    return [make_coordinates(image, left_average), make_coordinates(image, right_average)]

def make_central_line(image, lines):
    if lines[0] is None:
        middle_line = lines[1]
        x1,y1,x2,y2 = middle_line
        fit = np.polyfit((x1,x2),(y1,y2), 1)
        return [make_coordinates(image,fit), fit]
    if lines[1] is None:
        middle_line = lines[0]
        x1,y1,x2,y2 = middle_line
        fit = np.polyfit((x1,x2),(y1,y2), 1)
        return [make_coordinates(image,fit), fit]
    
    middle_line = np.average(lines, axis = 0)
    x1,y1,x2,y2 = middle_line
    fit = np.polyfit((x1,x2),(y1,y2), 1)
    return [make_coordinates(image,fit), fit]

def display_lines(image, lines, central_line):
    line_image = np.zeros_like(image)
    for line in lines:
        if line is not None:
            x1,y1,x2,y2 = line
            cv2.line(line_image, (x1,y1),(x2,y2),(0,0,255),5)
    x1,y1,x2,y2 = central_line
    cv2.line(line_image, (x1,y1),(x2,y2),(255,0,0),5)
    return line_image

def image_vision(img):
    ret, image = img.read()
    edges = canny(image)
    cropped_edges = region_of_interest(edges)
    lines = average_slope_intercept(image, find_lines(cropped_edges))
    if lines is not None:
        central_line = make_central_line(image, lines)
        line_image = display_lines(image, lines, central_line[0])
        combo_image = cv2.addWeighted(line_image, 0.8, image, 1, 1)
        show_img(combo_image, central_line[1])
        
def video_vision():
    image = cv2.VideoCapture('teste2.mp4')
    while image.isOpened():
        image_vision(image)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

video_vision()
