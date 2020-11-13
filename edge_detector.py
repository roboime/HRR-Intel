import numpy as np
import cv2


def flinha():
    image = cv2.imread('p5_1.jpg')
    # inserir o caminho da imagem manualmente
    hls = cv2.cvtColor(image, cv2.COLOR_BGR2HLS)
    lower = np.array([0, 0, 0])
    upper = np.array([255, 70, 255])

    blackmask = cv2.inRange(hls, lower, upper)
    kernel = np.ones((7, 7), np.uint8)
    opening = cv2.morphologyEx(blackmask, cv2.MORPH_OPEN, kernel)

    edges = cv2.Canny(opening, 150, 240, apertureSize=3)

    #cv2.imwrite('edges'+str(n+1)+".jpeg", edges)
    #cv2.imwrite('mask'+str(n+1)+".jpeg", blackmask)
    minLineLength = 100
    lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi/180, threshold=100,
                            lines=np.array([]), minLineLength=minLineLength, maxLineGap=20)

    a, b, c = lines.shape
    m = []
    b = []
    line_poly = []
    poly = [0, 0]
    right_lines = []
    left_lines = []
    print(len(lines))
    for i in range(len(lines)):
        ang = (180/np.pi)*np.arctan((lines[i][0][3] -
                                     lines[i][0][1])/(lines[i][0][2]-lines[i][0][0]))
        poly = [(lines[i][0][3]-lines[i][0][1])/(lines[i][0][2]-lines[i][0][0]), lines[i][0]
                [1]-((lines[i][0][3]-lines[i][0][1])/(lines[i][0][2]-lines[i][0][0]))*lines[i][0][0]]
        line_poly.append(poly)
        # print(ang)
    for i in range(len(line_poly)):
        ang = (180/np.pi)*np.arctan((lines[i][0][3] -
                                     lines[i][0][1])/(lines[i][0][2]-lines[i][0][0]))
        if abs(ang) > 20 and abs(ang) < 80:
            # cv2.line(image, (lines[i][0][0], lines[i][0][1]), (lines[i][0][2], lines[i][0][3]), (0, 0, 255), 3, cv2.LINE_AA)
            if line_poly[i][1] < 0:
                left_lines.append(line_poly[i])
            else:
                right_lines.append(line_poly[i])
    left_x = []
    right_x = []
    if len(left_lines) > 0:
        for j in range(len(left_lines)):
            left_x.append(560/left_lines[j][0] -
                          left_lines[j][1]/left_lines[j][0])
        x_main = min(left_x)
        k = left_x.index(x_main)
        left_average = left_lines[k]
    else:
        left_average = np.array([])
    if len(right_lines) > 0:
        for k in range(len(right_lines)):
            right_x.append(560/right_lines[k][0] -
                           right_lines[k][1]/right_lines[k][0])
        x_main = max(right_x)
        k = right_x.index(x_main)
        right_average = right_lines[k]
    else:
        right_average = np.array([])
    total_lines = [left_average, right_average]
    middle_line = np.average(lines, axis=0)
    print(middle_line)
    x1, y1, x2, y2 = middle_line[0][0], middle_line[0][1], middle_line[0][2], middle_line[0][3],
    fit = np.polyfit((x1, x2), (y1, y2), 1)
    return fit
