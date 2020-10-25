import math
import cv2
import numpy as np
import cv2
import numpy as np
import line_detector
import ob_detector


def rotate(image):
    x, y = ob_detector.xy(image)
    poly = line_detector.line_detector(image)
    x_central = poly[1] + poly[0]*y
    if x_central < x:
        print("esquerda")
        return 1
    else:
        print("direita")
        return 2
