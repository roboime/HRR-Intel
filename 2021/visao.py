import cv2
import numpy as np
import math


IMG_WIDTH = 0
RIGHT = 1
LEFT = -1

NAO_HA_RETA = 0
HA_DUAS_RETAS = 1
SO_ESQUERDA = 2
SO_DIREITA = 3


X1 = 0
Y1 = 1
X2 = 2
Y2 = 3
def coef_angular(lista):

    if lista[X2] != lista[X1]: return (math.atan((lista[Y2]-lista[Y1]) / (lista[X2]-lista[X1])))
    else: return 99999

def coef_linear(lista):
    return lista[Y1] - coef_angular(lista)*lista[X1]

class line():

    def __init__(self, segment):

        segment = segment.reshape(4)
        self.x1, self.y1, self.x2, self.y2 = segment

        side = (self.x1 + self.x2)/2 - IMG_WIDTH/2
        self.side = side / abs(side) # 1 para lado direito e -1 para lado esquerdo

        if self.x1 != self.x2:
            self.angCoef = (self.y2-self.y1)/(self.x2-self.x1)
            self.inc = math.atan(self.angCoef)
            self.linCoef = self.y1 - self.angCoef * self.x1
        else:
            self.linCoef = None
            self.angCoef = None
            self.inc = math.pi/2
    def get_y(self, x):
        return self.linCoef + self.angCoef * x


def white_mask(img):
    global IMG_WIDTH
    IMG_WIDTH = img.shape[1]

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) # converte a cor para hsv
    lower = np.array([0,0,140])   #range de cores em hsv para reconhecer as bordas
    upper = np.array([255,255,255])
    mask = cv2.inRange(hsv, lower, upper)

    kernel = np.ones((5,5), np.uint8) 
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=2)
    cv2.imwrite('edge.png', mask)
    return mask


def bordas_laterais_ebert(input_camera):
    edges = cv2.Canny(white_mask(input_camera), 75, 150) # destaca as linhas da imagem convertida em preto e branco
    segments = cv2.HoughLinesP(edges, 1, np.pi/180, 20, maxLineGap=20, minLineLength=50) # obtem os pontos que formam os segmentos de reta das linhas
    if segments is None: return [], [], 0 #não achou nenhum segmento de reta
    lines = []
    for segment in segments:
        l = line(segment) 
        lines.append(l)
    left_major = right_major = np.NINF
    left_edge = right_edge = None

    for l in lines:
        if l.angCoef is not None: # se não for inclinada de 90°
            if l.side*l.angCoef < 3.5 and l.side*l.angCoef > 2/7: #está dentro do range da inclinação
                r_intersect = l.get_y(IMG_WIDTH) # intersecção com a borda direita da imagem
                l_intersect = l.linCoef # intersecção com a borda esquerda da imagem

                if l.side == RIGHT and r_intersect > right_major:           #
                    right_major = r_intersect                               #
                    right_edge = l                                          #     a reta cuja intersecção com a borda lateral é
                if l.side == LEFT and l_intersect > left_major:             #     mais próxima da borda inferior será a borda lateral
                    left_major = l_intersect                                #     da pista
                    left_edge = l                                           #
    if left_edge is None and right_edge is None: return [], [], 0   # nenhuma das retas é borda da pista
    if left_edge is None: return [], [right_edge.angCoef, right_edge.linCoef], 2   # somente a borda da esquerda foi detectada
    if right_edge is None: return [left_edge.angCoef, left_edge.linCoef], [], 3 # somente a borda da direita foi detectada
    return [left_edge.angCoef, left_edge.linCoef], [right_edge.angCoef, right_edge.linCoef], 1 # as duas bordas da pista foram detectadas

def bordas_laterais(input_camera):
    img = input_camera
    np.zeros((728,1024,3), np.uint8)
    ##cria imagem toda preta para usar como fundo
     

    (altura, largura) = img.shape[:2] 
    centro = (largura // 2, altura // 2) 

    # Gerar matriz de rotação, em seguida transforma a imagem baseado em uma matriz
    M = cv2.getRotationMatrix2D(centro, 180, 1.0)  
    img = cv2.warpAffine(img, M, (largura, altura))

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) 
    mask = cv2.inRange(hsv, (0,3,117), (179,65,255)) 

    _, th = cv2.threshold(mask, 0, 255, cv2.THRESH_BINARY) 
    contours, _ = cv2.findContours(th, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    for contour in contours:
        area = cv2.contourArea(contour)
        if 1000000 > area > 50:
            approx = cv2.approxPolyDP(contour, 0.001*cv2.arcLength(contour, True), True)
            cv2.drawContours(preto, [approx], 0, (255, 255, 255), 2) 
            

    gray=cv2.cvtColor(preto,cv2.COLOR_BGR2GRAY)

    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength=50, maxLineGap=100)
    coordleft = []
    coordright =[]

    for line in lines:
        x1,y1,x2,y2= line[0]
        if ( y1>altura/2 or y2>altura/2) and 0.09<abs(((y2-y1)/(x2-x1))) and abs(((y2-y1)/(x2-x1)))<10:
            if ((y2-y1)/(x2-x1)) > 0:
                coordright.append([x1,y1,x2,y2])
                #cv2.line(img, (x1,y1), (x2,y2), (255,255,255), 2)
            else:
                coordleft.append([x1,y1,x2,y2])
                #cv2.line(img, (x1,y1), (x2,y2), (0,255,0), 2)
    
    ha_reta_na_direita = False

    if(len(coordright) != 0):
        ha_reta_na_direita = True
        coordright=np.array(coordright)
        mediaright = np.mean(coordright,axis=0)
        lista_media_direita = mediaright.tolist()
        mediaright=mediaright.astype(np.int64)
        [x1,y1,x2,y2]=mediaright
        #cv2.line(img, (x1,y1), (x2,y2), (0,0,255), 2)
        
    ha_reta_na_esquerda = False

    if(len(coordleft) != 0):
        ha_reta_na_esquerda = True
        coordleft=np.array(coordleft)
        medialeft = np.mean(coordleft,axis=0)
        lista_media_esquerda = medialeft.tolist()
        medialeft=medialeft.astype(np.int64)
        [x1,y1,x2,y2]=medialeft
        #cv2.line(img, (x1,y1), (x2,y2), (0,0,255), 2)
        #text= 'y_direita = '+str((y2-y1)/(x2-x1))+' *x + ' +str(y1-(((y2-y1)*x1)/(x2-x1)))
        #img = cv2.putText(img, text, (int(((x1+x2)/2))-450,int(((y1+y2)/2))), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)


    if ha_reta_na_direita == False and ha_reta_na_esquerda == False:
        return [],[],NAO_HA_RETA
    if ha_reta_na_direita == True and ha_reta_na_esquerda == True:
        return lista_media_esquerda, lista_media_direita, HA_DUAS_RETAS
    SO_ESQUERDA = 2
    if ha_reta_na_direita == False and ha_reta_na_esquerda == True:
       return lista_media_esquerda, [], SO_ESQUERDA
    SO_DIREITA = 3
    if ha_reta_na_direita == True and ha_reta_na_esquerda == False:
       return [], lista_media_direita, SO_DIREITA

    

   
# Essa funcao deve devolver o ponto medio ( (x,y) ) da borda inferior do obstaculo mais proximo
def ponto_medio_borda_inferior(imagem):
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

def calcular_porcentagem(valor_comparar):
    img = cv2.imread('./imagens/pista2.jpg') #trocar o diretorio da imagem
    #cv2.imwrite("imagem original.png", img)
    
    preto = cv2.imread('./imagens/pista2.jpg') #trocar o diretorio da imagem
    fundo = cv2.imread('./imagens/pista2.jpg') #trocar o diretorio da imagem
    preto = cv2.circle(preto, (0,0), 4000,(0,0) , -1) ##cria imagem toda preta do mesmo tamanho
    fundo = cv2.circle(preto, (0,0), 4000,(0,0) , -1) ##cria imagem toda preta do mesmo tamanho
    (altura, largura) = img.shape[:2] 
    centro = (largura // 2, altura // 2) 

        # Gerar matriz de rotação, em seguida transforma a imagem baseado em uma matriz
    M = cv2.getRotationMatrix2D(centro, 180, 1.0)  
    img = cv2.warpAffine(img, M, (largura, altura))
    #cv2.imwrite("invertendo a imagem.png", img)
    

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) ### muda as cores para o padrao
    mask = cv2.inRange(hsv, (0,53,16), (17,255,255)) ##cria a mascara
    kernel = np.ones((3,3), np.uint8) ##cria ao tal do kernel q eh uma matriz p andar na imagem
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel) ## tiras sugeirinhas fora, conforme o feedback atestou



    kernel = np.ones((3,3), np.uint8)
    mask = cv2.dilate(mask, kernel) ## tira os buracos de dentro
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel) 
    #cv2.imwrite("criado a mask.png", mask)
    



    _, th = cv2.threshold(mask, 0, 255, cv2.THRESH_BINARY) 
    contours, _ = cv2.findContours(th, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
   

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 500:
            approx = cv2.approxPolyDP(contour, 0.001*cv2.arcLength(contour, True), True)
            cv2.drawContours(preto, [approx], 0, (255, 255, 255), 2) 
            
            x,y,w,h = cv2.boundingRect(contour) ##pega as coordenadas do extremo inferior esquerdo e a altura e largura
            #cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2) ##desenha um retangulo


    #cv2.imwrite("contorno no preto.png", preto)
    
    gray=cv2.cvtColor(preto,cv2.COLOR_BGR2GRAY)
    #cv2.imwrite("gray.png",gray)
    
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    #cv2.imwrite("edges.png",edges)
   
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength=150, maxLineGap=900)
    print(lines)

    # indices para as coordenadas
    x1 = 0
    y1 = 1
    x2 = 2
    y2 = 3
    maximo = 0

    try:
        for i in range(0,100):
            coefienete_angular = abs((lines[i][0][y2]-lines[i][0][y1])/(lines[i][0][x1]-lines[i][0][x2]))
            if coefienete_angular < 1:
                cv2.line(img,(lines[i][0][x1],lines[i][0][y1]),(lines[i][0][x2],lines[i][0][y2]),(255,0,0),9)
                if(((lines[i][0][y1]+lines[i][0][y2])/2)>maximo):  
                    maximo = lines[i][0][y1]
            



    except:
        porcentagem = (maximo/altura)*100
        #print(maximo)
        if(porcentagem>valor_comparar):
            #cv2.imwrite("imagem com linhas.png", img)
            return True
        else:
            #cv2.imwrite("imagem com linhas.png", img)
            return False
