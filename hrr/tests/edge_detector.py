import numpy as np
import cv2
import os

def edge():
    image = cv2.imread(os.path.join("input_imgs", "i.jpg"))
    # inserir o caminho da imagem manualmente
    hls = cv2.cvtColor(image, cv2.COLOR_BGR2HLS)
    lower = np.array([0, 0, 0])
    upper = np.array([255, 75, 255])

    blackmask = cv2.inRange(hls, lower, upper)
    kernel = np.ones((7, 7), np.uint8)
    opening = cv2.morphologyEx(blackmask, cv2.MORPH_OPEN, kernel)

    edges = cv2.Canny(opening, 150, 240, apertureSize=3)

    cv2.imwrite("edges.jpg", edges)
    #cv2.imwrite('mask'+str(n+1)+".jpeg", blackmask)
    minLineLength = 150
    lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi/180, threshold=100,
                            lines=[], minLineLength=minLineLength, maxLineGap=20)

    a, b, c = lines.shape
    m = []
    b = []
    line_poly = []
    poly = [0, 0, 0]
    right_lines = []
    left_lines = []
    # print(len(lines))
    for i in range(len(lines)):
        ang = (180/np.pi)*np.arctan((lines[i][0][3] -
                                     lines[i][0][1])/(lines[i][0][2]-lines[i][0][0]))
        poly = [(lines[i][0][3]-lines[i][0][1])/(lines[i][0][2]-lines[i][0][0]), lines[i][0]
                [1]-((lines[i][0][3]-lines[i][0][1])/(lines[i][0][2]-lines[i][0][0]))*lines[i][0][0], lines[i][0]]
        line_poly.append(poly)
    for i in range(len(line_poly)):
        ang = (180/np.pi)*np.arctan((lines[i][0][3] -
                                     lines[i][0][1])/(lines[i][0][2]-lines[i][0][0]))
        if abs(ang) > 20 and abs(ang) < 80:
            if line_poly[i][0] < 0:
                left_lines.append(line_poly[i])
            else:
                right_lines.append(line_poly[i])

    left_x = []
    right_x = []
    if len(left_lines) > 0:
        for j in range(len(left_lines)):
            left_x.append(560/left_lines[j][0] -
                          left_lines[j][1]/left_lines[j][0])
        x_main = max(left_x)
        k = left_x.index(x_main)
        left_average = left_lines[k]
        rr = cv2.line(image, (left_average[2][0], left_average[2][1]), (
        left_average[2][2], left_average[2][3]), (0, 0, 255), 3, cv2.LINE_AA)
        cv2.imwrite("sssdd.jpg", rr)
    else:
        left_average = []
    if len(right_lines) > 0:
        for k in range(len(right_lines)):
            right_x.append(560/right_lines[k][0] -
                           right_lines[k][1]/right_lines[k][0])
        x_main = min(right_x)
        k = right_x.index(x_main)
        right_average = right_lines[k]
        cv2.line(rr, (right_average[2][0], right_average[2][1]), (
        right_average[2][2], right_average[2][3]), (0, 0, 255), 3, cv2.LINE_AA)
    else:
        right_average = []
    if left_average != [] and right_average != []:
        fit_1 = [left_average[0], left_average[1]]
        fit_2 = [right_average[0], right_average[1]]
        return fit_1, fit_2, 1
    if left_average == [] and right_average != []:
        fit = [right_average[0], right_average[1]]
        return [], fit, 2
    if left_average != [] and right_average == []:
        fit = [left_average[0], left_average[1]]
        return fit, [], 3
    if left_average == [] and right_average == []:
        fit = []
        return fit, [], 0
edge()