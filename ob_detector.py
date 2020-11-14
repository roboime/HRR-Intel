import cv2
import numpy as np


def xy():  # Argumento imagem #Retorno o ponto médio da linha mais baixa(xmed,ymed)
    image = cv2.imread('image_3\i2_2.jpg')

    # HLS filtro
    lower = np.array([5, 0, 0])
    upper = np.array([25, 255, 255])

    # A placa nos envia a imagem rotacionada, vamos então aqui rotacionar a imagem usando o centro como origem:
    (alt, lar) = image.shape[:2]  # captura altura e largura
    centro = (lar // 2, alt // 2)  # acha o centro

    M = cv2.getRotationMatrix2D(centro, 180, 1.0)  # Gerar matriz de rotação
    image = cv2.warpAffine(image, M, (lar, alt))  # Comando para rotacionar

    # image1 = cv2.blur(image, (7, 7))  # Suavizar a imagem utilizando blur

    hls = cv2.cvtColor(image, cv2.COLOR_BGR2HLS)  # Converter o COLORSPACE
    # Criação da mascara para objetos laranja
    orangemask = cv2.inRange(hls, lower, upper)

    # Usamos o canny para pegar os contornos
    edges = cv2.Canny(orangemask, 100, 300, apertureSize=3)

    # cv2.imwrite('edges'+str(n+1)+".jpeg",edges)
    # cv2.imwrite('mask'+str(n+1)+".jpeg",orangemask)

    minLineLength = 90  # Parametro da HoughLines

    # Utlizar HoughLinesP para retornar x1 y1 x2 y2
    lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi/180, threshold=100,
                            lines=np.array([]), minLineLength=minLineLength, maxLineGap=200)

    # a = número de linhas (matriz)
    # b = número de linhas da lista
    # c = 4, pois é a DIM

    a, b, c = lines.shape

    # A padronização dos eixos no OpenCV é o eixo y para baixo, portanto ymax=-1 da sempre valores maiores que os medidos
    maxy = -1

    linha_objeto = []
    for i in range(a):
        if lines[i][0][1] > maxy or lines[i][0][3] > maxy:
            maxy = max(lines[i][0][1], lines[i][0][3])
            indice = i

    linha_objeto = lines[indice][0]

    if linha_objeto != []:
        medy = (linha_objeto[1]+linha_objeto[3])/2  # Ponto médio em y
        medx = (linha_objeto[0]+linha_objeto[2])/2  # Ponto médio em x
    else:
        medy = 0
        medx = 0
    return medx, medy
