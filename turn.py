# adaptado para utilizar no notebook
import math
import cv2
import numpy as np
import cv2
import numpy as np
import edge_detector
import obj_detector
#import picamera
from time import sleep


def rotate():
    #camera = picamera.PiCamera()
    # camera.start_preview()
    # sleep(2.5)
    #image = camera.capture('/home/pi/image.jpg')
    # camera.stop_preview()
    x, y = obj_detector.xy()
    poly_left, poly_right, j = edge_detector.edge()

    # inserir o caminho da imagem manualmente
    # j = 1: linha central. j = 2: borda direita. j = 3: borda esquerda. j = 0: nenhuma borda
    pixel_scale = 20.4
    d_min = 40
    x_robot = 0
    if x == 0 and y == 0:
        # Não detectou obstáculo
        return 0
    else:
        if j == 1:
            poly_inv_left = [1/poly_left[0], -poly_left[1]/poly_left[0]]
            x_linha_left = poly_inv_left[1] + poly_inv_left[0]*y
            poly_inv_right = [1/poly_right[0], -poly_right[1]/poly_right[0]]
            x_linha_right = poly_inv_left[1] + poly_inv_left[0]*y
            d_left = abs(x - x_linha_left)/pixel_scale
            d_right = abs(x - x_linha_right)/pixel_scale
            ang_left = np.arctan(poly_left[0])*(180/np.pi)
            ang_right = np.arctan(poly_right[0])*(180/np.pi)
            # 1 para esquerda, 2 direita, 3 centro
            if abs(ang_left) >= abs(ang_right) + 10:
                x_robot = 1
            elif abs(ang_right) >= abs(ang_left) + 10:
                x_robot = 2
            else:
                x_robot = 3
            print(x_robot)
            if x_robot == 3:
                if d_left > d_min and d_right > d_min:
                    d = max(d_left, d_right)
                    if d == d_left:
                        return 1
                    else:
                        return 2
                elif d_left > d_min and d_right <= d_min:
                    return 1
                elif d_left <= d_min and d_right > d_min:
                    return 2
                else:
                    d = max(d_left, d_right)
                    if d == d_left:
                        return 1
                    else:
                        return 2
            if x_robot == 1:
                if d_left < d_min:
                    return 2
                else:
                    return 1
            if x_robot == 2:
                if d_right < d_min:
                    return 1
                else:
                    return 2
        if j == 2:
            poly_inv = [1/poly_right[0], -poly_right[1]/poly_right[0]]
            x_linha = poly_inv[1] + poly_inv[0]*y
            if abs(x - x_linha) > d_min*pixel_scale:
                return 2
            else:
                return 1
        if j == 3:
            poly_inv = [1/poly_left[0], -poly_left[1]/poly_left[0]]
            x_linha = poly_inv[1] + poly_inv[0]*y
            if abs(x - x_linha) > d_min*pixel_scale:
                return 1
            else:
                return 2
        # if j == 0:
