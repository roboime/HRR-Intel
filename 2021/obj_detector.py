import cv2
import numpy as np

#retorna (x,y) do "pe" do obstaculo mais proximo
def ponto_medio_borda_inferior():
    imagem = cv2.imread('image_3\i2_2.jpg')
    (altura, largura) = imagem.shape[:2] 
    centro = (largura // 2, altura // 2) 

    # Gerar matriz de rotação, em seguida transforma a imagem baseado em uma matriz
    M = cv2.getRotationMatrix2D(centro, 180, 1.0)  
    imagem = cv2.warpAffine(imagem, M, (largura, altura))

    #blur opcional
    # imagem = cv2.blur(imagem, (7, 7))

    imagem_hls = cv2.cvtColor(imagem, cv2.COLOR_BGR2HLS)
    limite_inf_filtro_laranja = np.array([5, 0, 0])
    limite_sup_filtro_laranja = np.array([25, 255, 255])
    orangemask = cv2.inRange(imagem_hls, limite_inf_filtro_laranja, limite_sup_filtro_laranja)

    # Usamos "Canny" para pegar os contornos
    lista_bordas = cv2.Canny(orangemask, 100, 300, apertureSize=3)


    minLineLength = 90  # Parametro da HoughLines

    # Utlizar HoughLinesP para retornar (x1,y1) (x2,y2)
    segmentos = cv2.HoughLinesP(lista_bordas, rho=1, theta=np.pi/180, threshold=100,
                            lines=np.array([]), minLineLength=minLineLength, maxLineGap=200)

    
    #se quisermos visualizar
    '''for segmento in segmentos:
        x1,y1,x2,y2= segmento[0]
        cv2.line(imagem, (x1,y1), (x2,y2), (0,255,0), 2)'''

    numero_segmentos, _, _ = segmentos.shape

    #legenda de indices importantes em segmentos
    x1 = 0
    y1 = 1
    x2 = 2
    y2 = 3

    ymed_bloco_todo = 0
    for i in range(numero_segmentos):
        ymed_bloco_todo+=segmentos[i][0][1] + segmentos[i][0][3]
    ymed_bloco_todo/=2*numero_segmentos

    y_max = -1
    x_min = largura
    x_max = 0
    #esse fator para baixo serve para procurar segmentos ainda mais abaixo do ponto medio
    fator_para_baixo = 1.3

    for i in range(numero_segmentos):
        if ((segmentos[i][0][y1]+segmentos[i][0][y2])/2 > ymed_bloco_todo*fator_para_baixo):
            x_min = min(x_min, segmentos[i][0][x1], segmentos[i][0][x2])
            x_max = max(x_max, segmentos[i][0][x1], segmentos[i][0][x2])
            y_max = max(y_max, segmentos[i][0][y1], segmentos[i][0][y2])
    x_med = (x_min + x_max) / 2

    ##feedback
    '''imagem = cv2.circle(imagem, (int(largura//2),int(fator_para_baixo*ymed_bloco_todo)), 50,(0,255,0) , -1)
    imagem = cv2.circle(imagem, (int(x_min),int(y_max)), 50,(0,255,0) , -1)
    imagem = cv2.circle(imagem, (int(x_max),int(y_max)), 50,(0,255,0) , -1)
    imagem = cv2.circle(imagem, (int(x_med),int(y_max)), 50,(255,0,0) , -1)
    little = cv2.resize(imagem, (960, 540)) 
    cv2.imshow("com o ponto medio", little)
    cv2.waitKey()'''
    return x_med, y_max

