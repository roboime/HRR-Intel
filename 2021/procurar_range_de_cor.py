""" Programa para calibrar os ranges de cor utilizados para reconhecer a pista e os obstáculos pelo robo.
    Siga os passos para utiliza-lo:

    1 - Coloque o path correto da imagem na variavel global PATH.
    2 - Execute o programa. Abrira 4 imagens divididas numa janela que estara escrito a cor que deve ser mascarada a imagem e
    um track bar para ajustar os ranges.
    3 - Ajuste os ranges. Ao terminar, aperte Esc para passar para a proxima cor.
    4 - Repita o passo 3 ate o programa encerrar.
    
    O arquivo com os ranges estara salvo no mesmo diretorio com o nome ranges_<cor>.txt. O path para este arquivo pode ser
    passado no metodo mask() da Classe_imagem() para obter a mascara relativa a cor"""

import cv2
import numpy as np

PATH = "sla.png"
CORES = ["LARANJA", "VERMELHO", "BRANCO"]
FILES = ["ranges_laranja.txt", "ranges_vermelho.txt", "ranges_branco.txt"]

def empty(a):
    pass


def stackImages(scale, imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range(0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape[:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]),
                                                None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y] = cv2.cvtColor(imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank] * rows
        hor_con = [imageBlank] * rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None, scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor = np.hstack(imgArray)
        ver = hor
    return ver

def main():
    for cor in CORES:
        with open(FILES[CORES.index(cor)], "r") as f:
            lines = f.readlines()
            cur = lines[0].split(",")
            cv2.namedWindow("TrackBars")
            cv2.resizeWindow("TrackBars", 640, 240)
            cv2.createTrackbar("Hue Min", "TrackBars", int(cur[0]), 179, empty)
            cv2.createTrackbar("Hue Max", "TrackBars", int(cur[3]), 179, empty)
            cv2.createTrackbar("Sat Min", "TrackBars", int(cur[1]), 255, empty)
            cv2.createTrackbar("Sat Max", "TrackBars", int(cur[4]), 255, empty)
            cv2.createTrackbar("Val Min", "TrackBars", int(cur[2]), 255, empty)
            cv2.createTrackbar("Val Max", "TrackBars", int(cur[5]), 255, empty)


        while True:
            img = cv2.imread(PATH)
            imgHSV = cv2.cvtColor(img, cv2. COLOR_BGR2HSV)
            h_min = cv2.getTrackbarPos("Hue Min", "TrackBars")
            h_max = cv2.getTrackbarPos("Hue Max", "TrackBars")
            s_min = cv2.getTrackbarPos("Sat Min", "TrackBars")
            s_max = cv2.getTrackbarPos("Sat Max", "TrackBars")
            v_min = cv2.getTrackbarPos("Val Min", "TrackBars")
            v_max = cv2.getTrackbarPos("Val Max", "TrackBars")
            # print(h_min, h_max, s_min, s_max, v_min, v_max)
            lower = np.array([h_min, s_min, v_min])
            upper = np.array([h_max, s_max, v_max])
            mask = cv2.inRange(imgHSV, lower, upper)
            imgResult = cv2.bitwise_and(img, imgHSV)
            # cv2.imshow("Mask", mask)
            # cv2.imshow("Result", imgResult)

            imgStack = stackImages(0.3, ([img, imgHSV], [mask, imgResult]))
            little = cv2.resize(imgStack, (960, 540))
            cv2.imshow("Ranges do " + cor, little)
            
            with open(FILES[CORES.index(cor)], "w") as f:
                f.write(str(lower[0])+","+str(lower[1])+","+str(lower[2])+","+str(upper[0])+","+str(upper[1])+","+str(upper[2]))
            k = cv2.waitKey(33)
            if k==27:    # Esc key to stop
                break
if __name__ == "__main__": main()