import cv2
import numpy as np
import math
from constantes import *
from os import listdir
from os.path import  join
from camera import RaspCamera


path = "./tests/imagens/input_imgs/"

IMAGES = [Classe_imagem(cv2.imread(join(path, f))) for f in listdir(join(path))]

font                   = cv2.FONT_HERSHEY_SIMPLEX


""" Classe relacionada a imagem obtida pela camera. Ao ser chamada, inverte a imagem e salva constantes relacionadas a imagem, como altura, largura e centro.
 Possui o metodo mask, que retorna a mascara da imagem, passando o arquivo onde esta salvo os ranges da cor."""
class Classe_imagem():
    def __init__(self, path):
        #print("Entrando no _init_ do Classe_imagem()")
        img = cv2.imread(path)
        #img = np.array(img)

        img = cv2.rotate(img, cv2.ROTATE_180)
        #cv2.imwrite("/home/pi/Pictures/imagem_girada.jpg", img)

        img.astype(np.uint8)

        (self.altura, self.largura) = img.shape[:2] 
        self.centro = ( (self.largura)/2, (self.altura)/2 )

        self.img = img
        self.topo_da_pista = 0
        self.meio_da_pista = 0 # coordenada x do meio da pista
        self.largura_pista = 0 # largura do final da pista na imagem
        self.mult_largura_pista = 0.7 #ate quanto da metade da largura da pista ainda eh atravessavel pelo robo

    def mask(self, ranges_file_path):
        hsv = cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV) # converte a cor para hsv
        with open(ranges_file_path, "r") as f:
            lines = f.readlines()
            range = lines[0].split(",")
            lower = np.array([int(range[0]),int(range[1]),int(range[2])])  #range de cores em hsv para reconhecer as bordas
            upper = np.array([int(range[3]),int(range[4]),int(range[5])])
        mask = cv2.inRange(hsv, lower, upper)
        kernel = np.ones((5,5), np.uint8) 
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=1)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
        return mask

'''tira o coeficiente angular ( delta y / delta x) a partir de uma lista de coordenadas x1 y1 x2 y2. utilizada em funcoes 
dessa biblioteca: '''
def coef_angular(lista):
    if len(lista) != 0:
        if lista[X2] != lista[X1]: return float(float(lista[Y2]-lista[Y1]) / float(lista[X2]-lista[X1]))
        else: return 999.9
    else: return 999.9


'''tira o coeficiente linear ( y1 - coef_angular *x1 = coef_linear) a partir de uma lista de coordenadas x1 y1 x2 y2. 
utilizada em funcoes dessa biblioteca: '''
def coef_linear(lista):
    if len(lista) != 0:
        return float(float(lista[Y1]) - float(lista[X1])*coef_angular(lista))
    else:   return 0
# Essa funcao deve devolver o ponto medio ( (x,y) ) da borda inferior do obstaculo mais proximo


""" recebe a mascara do branco e o objeto_imagem e procura o contorno fechado de maior area (pista). salva o y da pista como topo_da_pista e o x + largura/2
 como o meio_da_pista no objeto_imagem"""
def reconhecer_pista(mask, objeto_imagem):
    _, th = cv2.threshold(mask, 0, 255, cv2.THRESH_BINARY) 
    contours, _ = cv2.findContours(th, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[-2:]
    if len(contours) != 0 :
        m2 = m1 = contours[0]
        
        for contour in contours:
            _,y,_,_ = cv2.boundingRect(contour)
            area = cv2.contourArea(contour)
            if y > objeto_imagem.altura//2 and area > 50000 and area > cv2.contourArea(m1):
                m1 = contour
        for contour in contours:
            _,y,_,_ = cv2.boundingRect(contour)
            area = cv2.contourArea(contour)
            if y > objeto_imagem.altura//2 and area > 50000 and area > cv2.contourArea(m2) and m2 != m1:
                m2 = contour
        
                
        x1,y1,w1,h1 = cv2.boundingRect(m1)
        x2,y2,w2,h2 = cv2.boundingRect(m2)
        objeto_imagem.topo_da_pista = (y1+y2)//2
        objeto_imagem.meio_da_pista = (x1+x2)//2
    else:
        objeto_imagem.topo_da_pista = objeto_imagem.altura//2
        objeto_imagem.meio_da_pista = objeto_imagem.largura//2
    cv2.rectangle(objeto_imagem.img, (x1, y1), (x1+w1, y1+h1), (0, 0, 0), thickness=3)
    cv2.rectangle(objeto_imagem.img, (x2, y2), (x2+w2, y2+h2), (0, 0, 0), thickness=3)
   # objeto_imagem.img = cv2.line(objeto_imagem.img, (objeto_imagem.meio_da_pista, objeto_imagem.topo_da_pista), (objeto_imagem.meio_da_pista, objeto_imagem.altura), (0, 255, 255), 2)
    objeto_imagem.img = cv2.line(objeto_imagem.img, (0, objeto_imagem.topo_da_pista), (objeto_imagem.largura, objeto_imagem.topo_da_pista), (0, 255, 255), 2)


""" recebe duas retas no formato [x1, y1, x2, y2] e retora o ponto de interseccao x, y """
def interscetion(r1, r2):
    ml = coef_angular(r1)
    mr = coef_angular(r2)
    nl = coef_linear(r1)
    nr = coef_linear(r2)

    x = (nr-nl)/(ml-mr)
    y = mr*x+nr
    #IMG = cv2.circle(IMG, (int(x),int(y)), radius=10, color=(0, 255, 255), thickness=-1)
    return int(x), int(y)   


''' identifica a borda laranja mais baixa e traca o ponto medio dela, retornando-o. Usada na decisao desvio'''
def ponto_medio_borda_inferior(objeto_imagem):
    print("Entrou na ponto medio borda inferior")
    orangemask = objeto_imagem.mask("ranges_laranja.txt")
  #  cv2.imwrite( path+"../masks/"+str(ind)+".png", orangemask)
    largura = objeto_imagem.largura
    # Usamos "Canny" para pegar os contornos
    
    #_, th = cv2.threshold(orangemask, 0, 255, cv2.THRESH_BINARY) 
  #  contours, _ = cv2.findContours(th, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[-2:]
  #  
   # if len(contours) == 0: return 0,0, 0
   # mais_proximo = contours[0]
  #  for contour in contours:
  #      x, y, w, h = cv2.boundingRect(contour)

    lista_bordas = cv2.Canny(orangemask, 100, 300, apertureSize=3)

    minLineLength = 90  # Parametro da HoughLines
    
    # Utlizar HoughLinesP para retornar (x1,y1) (x2,y2)
    #segmentos = cv2.HoughLinesP(lista_bordas, rho=1, desvio_maximo=np.pi/180, threshold=100, lines=np.array([]), minLineLength=minLineLength, maxLineGap=10)
    segmentos = cv2.HoughLinesP(lista_bordas, 1, np.pi/180, 100, minLineLength=50, maxLineGap=100)
    if segmentos is None: return 0,0,0
    numero_segmentos, _, _ = segmentos.shape
    if numero_segmentos == 0: return 0,0, 0
    
    #se quisermos visualizar
    '''for segmento in segmentos:
        x1,y1,x2,y2= segmento[0]
        cv2.line(imagem, (x1,y1), (x2,y2), (0,255,0), 2)'''

    """y_med_max = 0
    borda_inferior = segmentos[0]
    for segmento in segmentos:
        segmento = segmento.reshape(4)
        x1, y1, x2, y2 = segmento
        y_med = (y1+y2)//2
        if y_med > y_med_max:
            y_med_max = y_med
            borda_inferior = segmento
    x1, y1, x2, y2 = borda_inferior
    x_med = (x1 + x2)//2
    cv2.line(objeto_imagem.img, (x1,y1), (x2,y2), (0,0,255), 2)
    objeto_imagem.img = cv2.circle(objeto_imagem.img, (x_med, y_med_max), radius=10, color=(0, 255, 255), thickness=-1)
    return x_med , y_med_max"""

    ymed_bloco_todo = 0
    for i in range(numero_segmentos):
        ymed_bloco_todo+=segmentos[i][0][1] + segmentos[i][0][3]
    ymed_bloco_todo//=2*numero_segmentos
    y_max = -1
    x_min = largura
    x_max = 0
    #esse fator para baixo serve para procurar segmentos ainda mais abaixo do ponto medio
    fator_para_baixo = 1.3
    cv2.line(objeto_imagem.img, (0,int(ymed_bloco_todo*fator_para_baixo)), (objeto_imagem.largura,int(ymed_bloco_todo*fator_para_baixo)), (255,0,0), 2)

    for i in range(numero_segmentos):
        x1, y1, x2, y2 = segmentos[i].reshape(4)
   #     cv2.line(objeto_imagem.img, (x1,y1), (x2,y2), (255,0,255), 2)
        if (segmentos[i][0][Y1] > ymed_bloco_todo*fator_para_baixo or segmentos[i][0][Y2] > ymed_bloco_todo*fator_para_baixo):
            x_min = min(x_min, segmentos[i][0][X1], segmentos[i][0][X2])
            x_max = max(x_max, segmentos[i][0][X1], segmentos[i][0][X2])
            y_max = max(y_max, segmentos[i][0][Y1], segmentos[i][0][Y2])
    x_med = (x_min + x_max) // 2
    ##feedback
    '''imagem = cv2.circle(imagem, (int(largura//2),int(fator_para_baixo*ymed_bloco_todo)), 50,(0,255,0) , -1)
    imagem = cv2.circle(imagem, (int(x_min),int(y_max)), 50,(0,255,0) , -1)
    imagem = cv2.circle(imagem, (int(x_max),int(y_max)), 50,(0,255,0) , -1)
    imagem = cv2.circle(imagem, (int(x_med),int(y_max)), 50,(255,0,0) , -1)
    little = cv2.resize(imagem, (960, 540)) 
    cv2.imshow("com o ponto medio", little)
    cv2.waitKey()'''
    cv2.line(objeto_imagem.img, (x_min,y_max), (x_max,y_max), (0,0,255), 2)
    objeto_imagem.img = cv2.circle(objeto_imagem.img, (x_med, y_max), radius=10, color=(0, 255, 255), thickness=-1)
    print("Saindo ponto medio borda inferior")
    return x_min, x_max, y_max


'''Recebe apenas a imagem. Retorna o x1 y1 x2 y2 das bordas laterais e uma variavel auxiliar que inidica se
foram encontrada, duas retas, zero retas ou uma reta ( e qual eh ela). Versao do fernandes que utiliza uma mascara branca
e uma area branca nao tao grande para tentar pegar a parte mais externa das bordas pretas, alem de filtrar as muito
deitadas ou muito verticais. Usada na alinhamento_pista e na decisao_desvio'''
def bordas_laterais_v1(objeto_imagem):
    img = objeto_imagem.img
    largura, altura = objeto_imagem.largura, objeto_imagem.altura
    preto = np.zeros((largura, altura, 3), np.uint8)
    mask = objeto_imagem.mask("ranges_preto.txt")

    _, th = cv2.threshold(mask, 0, 255, cv2.THRESH_BINARY) 
    contours, _ = cv2.findContours(th, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[-2:]
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
    if lines is not None:
        for line in lines:
            x1,y1,x2,y2= line[0]
            if ( y1>altura/4 or y2>altura/4) and np.tan(math.radians(2))<abs(((y2-y1)/(x2-x1))) and abs(((y2-y1)/(x2-x1)))*np.tan(math.radians(88)):
                if ((y2-y1)/(x2-x1)) > 0:
                    coordright.append([x1,y1,x2,y2])
                    cv2.line(img, (x1,y1), (x2,y2), (255,255,255), 2)
                else:
                    coordleft.append([x1,y1,x2,y2])
                    cv2.line(img, (x1,y1), (x2,y2), (0,255,0), 2)
    else: return [],[],NAO_HA_RETA
    ha_reta_na_direita = False

    if(len(coordright) != 0):
        ha_reta_na_direita = True
        coordright=np.array(coordright)
        mediaright = np.mean(coordright,axis=0)
        lista_media_direita = mediaright.tolist()
        mediaright=mediaright.astype(np.int64)
        [x1,y1,x2,y2]=mediaright
        cv2.line(img, (x1,y1), (x2,y2), (0,0,255), 2)
        
    ha_reta_na_esquerda = False

    if(len(coordleft) != 0):
        ha_reta_na_esquerda = True
        coordleft=np.array(coordleft)
        medialeft = np.mean(coordleft,axis=0)
        lista_media_esquerda = medialeft.tolist()
        medialeft=medialeft.astype(np.int64)
        [x1,y1,x2,y2]=medialeft
        cv2.line(img, (x1,y1), (x2,y2), (0,0,255), 2)
        #text= 'y_direita = '+str((y2-y1)/(x2-x1))+' *x + ' +str(y1-(((y2-y1)*x1)/(x2-x1)))
        #img = cv2.putText(img, text, (int(((x1+x2)/2))-450,int(((y1+y2)/2))), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)

    cv2.imwrite("./tests/bordas_v2.jpg", img)
    if ha_reta_na_direita == False and ha_reta_na_esquerda == False:
        return [],[],NAO_HA_RETA
    if ha_reta_na_direita == True and ha_reta_na_esquerda == True:
        return lista_media_esquerda, lista_media_direita, HA_DUAS_RETAS
    if ha_reta_na_direita == False and ha_reta_na_esquerda == True:
       return lista_media_esquerda, [], SO_ESQUERDA
    return [], lista_media_direita,SO_DIREITA


""" adaptacao da bordas_laterais_v1 que adiciona 3 restricoes para encontrar as retas. A primeira eh a RANGE_INCLINACAO, que seleciona um coeficiente angular minimo
 e maximo para considerar como borda. A segunda eh o topo_da_pista, que seleciona apenas as retas que estao abaixo do topo da pista para evitar ruidos. A terceira
  eh o meio_da_pista que divide as retas da borda da esquerda e da borda da direita."""
def bordas_laterais_v2(objeto_imagem):
    mask = objeto_imagem.mask("ranges_preto.txt")
   # reconhecer_pista(mask, objeto_imagem)
    img = objeto_imagem.img
    edges = cv2.Canny(mask, 50, 150, apertureSize=3)
    cv2.imwrite("./tests/mask.png", mask)

    lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=40, minLineLength=10, maxLineGap=50)
  #  lines = cv2.HoughLinesP(mask, 1, np.pi/180, threshold=100, minLineLength=10, maxLineGap=20)
    left_lines = []
    right_lines =[]
   # todas_as_linhas = IMG
    if lines is not None:
        for line in lines:
            line = line.reshape(4)
            x1,y1,x2,y2 = line
            img = cv2.line(img, (x1,y1), (x2,y2), (0,127,255), 2)
        	
            desvio_maximo = np.pi/180*RANGE_INCLINACAO
            #print("topo da imagem", objeto_imagem.topo_da_pista)
            #printa("range inclinacao", RANGE_INCLINACAO)
            #print("pontos: ", line)
            #print("coef_angular: ", coef_angular(line))
            #print("angulo: ", 180/np.pi*math.atan(coef_angular(line)))
            if y1>objeto_imagem.topo_da_pista or y2>objeto_imagem.topo_da_pista:
                if math.atan(1)-desvio_maximo/2 < math.atan(coef_angular(line)) < math.atan(1)+desvio_maximo/2:
                    right_lines.append([x1,y1,x2,y2])
                #    print("angulo : ", 180/np.pi*math.atan(coef_angular(line)))
                  #  print([x1, y1, x2, y2])
                    cv2.line(objeto_imagem.img, (x1,y1), (x2,y2), (0,255,0), 2)
                if math.atan(-1)-desvio_maximo/2 < math.atan(coef_angular(line)) < math.atan(-1)+desvio_maximo/2:
                    left_lines.append([x1,y1,x2,y2])
                    cv2.line(objeto_imagem.img, (x1,y1), (x2,y2), (0,127,0), 2)
    else: return [],[],NAO_HA_RETA
   # cv2.imwrite("todas_as_linhas.png", todas_as_linhas)

    ha_reta_na_direita = False
    if(len(right_lines) != 0):
        ha_reta_na_direita = True
        vertical_direita = [objeto_imagem.largura,0,objeto_imagem.largura,objeto_imagem.altura]
        y_max = 0
        right = right_lines[0]
        for line in right_lines:
            _,y = interscetion(line, vertical_direita)
            if y > y_max:
                y_max = y
                right = line
        [x1, y1, x2, y2] = right
        cv2.line(objeto_imagem.img, (x1,y1), (x2,y2), (0,0,255), 2)
        
    ha_reta_na_esquerda = False
    if(len(left_lines) != 0):
        ha_reta_na_esquerda = True
        vertical_esquerda = [0,0,0,objeto_imagem.altura]
        y_max = 0
        left = left_lines[0]
        for line in left_lines:
            _,y = interscetion(line, vertical_esquerda)
            if y > y_max:
                y_max = y
                left = line
        [x1, y1, x2, y2] = left
        cv2.line(objeto_imagem.img, (x1,y1), (x2,y2), (0,0,255), 2)

    cv2.imwrite("./tests/bordas_laterais.jpg", objeto_imagem.img)
    if ha_reta_na_direita == False and ha_reta_na_esquerda == False:
        return [],[],NAO_HA_RETA
    if ha_reta_na_direita == True and ha_reta_na_esquerda == True:
        return left, right, HA_DUAS_RETAS
    if ha_reta_na_direita == False and ha_reta_na_esquerda == True:
        return left, [], SO_ESQUERDA
    if ha_reta_na_direita == True and ha_reta_na_esquerda == False:
        return [], right, SO_DIREITA



#dado uma imagem e um valor de comparacao, verificar se a reta mais proxima esta dentro do limite ou nao 
def checar_proximidade(valor_comparar, imagem_path):

    #objeto_imagem = camera.Take_photo()
    #input_imagem = imagem_path + ".img"
    objeto_imagem = Classe_imagem(imagem_path)
    #img = objeto_imagem.copy() #funcao para pegar a imagem e armazena-la
    #cv2.imwrite("imagem original.png", img)
    
    #preto = objeto_imagem.copy() #criar uma imagem reserva

    largura, altura = objeto_imagem.largura, objeto_imagem.altura
    preto = np.zeros((largura, altura, 3), np.uint8)

    #preto = cv2.circle(objeto_imagem, (0,0), 4000,(0,0) , -1) ##cria imagem toda preta do mesmo tamanho
    
    mask = objeto_imagem.mask("ranges_vermelho.txt")
    #cv2.imwrite("criado a mask.png", mask)

    _, th = cv2.threshold(mask, 0, 255, cv2.THRESH_BINARY) 
    contours, _ = cv2.findContours(th, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[-2:]

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 500:##pegar os contornos com um tamanho minimo para evitar ruidos
            approx = cv2.approxPolyDP(contour, 0.001*cv2.arcLength(contour, True), True)
            cv2.drawContours(preto, [approx], 0, (255, 255, 255), 2) ##desenhar os contornos na imagem preta, para ter uma imagem so com os contornos
            
            x,y,w,h = cv2.boundingRect(contour) ##pega as coordenadas do extremo inferior esquerdo e a altura e largura
            #cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2) ##desenha um retangulo


    #cv2.imwrite("contorno no preto.png", preto)
    
    gray=cv2.cvtColor(preto,cv2.COLOR_BGR2GRAY)
    #cv2.imwrite("gray.png",gray)
    
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    #cv2.imwrite("edges.png",edges)
   
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength=150, maxLineGap=900)#criar um vetor com dois pontos(coordenadas x e y de cada ponto) para determinar uma reta
    #print(lines)

    # indices para as coordenadas
    x1 = 0
    y1 = 1
    x2 = 2
    y2 = 3
    maximo = 0

    try:
        for i in range(0,100):
            coefienete_angular = abs((lines[i][0][y2]-lines[i][0][y1])/(lines[i][0][x1]-lines[i][0][x2]))
            if coefienete_angular < 1:#eliminar retas muito inclinadas pq queremos retas horizontais
                #cv2.line(img,(lines[i][0][x1],lines[i][0][y1]),(lines[i][0][x2],lines[i][0][y2]),(255,0,0),9)
                if(((lines[i][0][y1]+lines[i][0][y2])/2)>maximo):  #encontrar a reta mais proxima do robo, por meio da coordenada y
                    maximo = lines[i][0][y1]

    except:#quando ele nao encontrar mais nenhuma reta no vetor line, ele vai dar erro e vir para essa parte do codigo. 
        porcentagem = 100 - ((maximo/altura)*100)
        #print(maximo)
        print("A porcentagem eh: {}".format(porcentagem))
        if(porcentagem<valor_comparar):
            print("obstaculo proximo")
            #cv2.imwrite("imagem com linhas.png", img)
            return True
        else:
            print("obstaculo ainda distante")
            #cv2.imwrite("imagem com linhas.png", img)
            return False
def bordas_laterais_v2(objeto_imagem):
    mask = objeto_imagem.mask("ranges_branco.txt")
   # reconhecer_pista(mask, objeto_imagem)
    img = objeto_imagem.img
    edges = cv2.Canny(mask, 50, 150, apertureSize=3)
    cv2.imwrite("./tests/mask.png", mask)

    lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=40, minLineLength=10, maxLineGap=50)
  #  lines = cv2.HoughLinesP(mask, 1, np.pi/180, threshold=100, minLineLength=10, maxLineGap=20)
    left_lines = []
    right_lines =[]
   # todas_as_linhas = IMG
    if lines is not None:
        for line in lines:
            line = line.reshape(4)
            x1,y1,x2,y2 = line
            img = cv2.line(img, (x1,y1), (x2,y2), (0,127,255), 2)
        	
            desvio_maximo = np.pi/180*RANGE_INCLINACAO
            #print("topo da imagem", objeto_imagem.topo_da_pista)
            #print("range inclinacao", RANGE_INCLINACAO)
            #print("pontos: ", line)
            #print("coef_angular: ", coef_angular(line))
            #print("angulo: ", 180/np.pi*math.atan(coef_angular(line)))
            if y1>objeto_imagem.topo_da_pista or y2>objeto_imagem.topo_da_pista:
                if math.atan(1)-desvio_maximo/2 < math.atan(coef_angular(line)) < math.atan(1)+desvio_maximo/2 and (x1 >= objeto_imagem.largura//2 or x2 >= objeto_imagem.largura//2):
                    right_lines.append([x1,y1,x2,y2])
                #    print("angulo : ", 180/np.pi*math.atan(coef_angular(line)))
                  #  print([x1, y1, x2, y2])
                    cv2.line(objeto_imagem.img, (x1,y1), (x2,y2), (0,255,0), 2)
                if math.atan(-1)-desvio_maximo/2 < math.atan(coef_angular(line)) < math.atan(-1)+desvio_maximo/2 and (x1 < objeto_imagem.largura//2 or x2 < objeto_imagem.largura//2):
                    left_lines.append([x1,y1,x2,y2])
                    cv2.line(objeto_imagem.img, (x1,y1), (x2,y2), (0,127,0), 2)
    else: return [],[],NAO_HA_RETA
   # cv2.imwrite("todas_as_linhas.png", todas_as_linhas)

    ha_reta_na_direita = False
    if(len(right_lines) != 0):
        ha_reta_na_direita = True
        vertical_direita = [objeto_imagem.largura,0,objeto_imagem.largura,objeto_imagem.altura]
        y_max = 0
        right = right_lines[0]
        for line in right_lines:
            _,y = interscetion(line, vertical_direita)
            if y > y_max:
                y_max = y
                right = line
        [x1, y1, x2, y2] = right
        cv2.line(objeto_imagem.img, (x1,y1), (x2,y2), (0,0,255), 2)
        
    ha_reta_na_esquerda = False
    if(len(left_lines) != 0):
        ha_reta_na_esquerda = True
        vertical_esquerda = [0,0,0,objeto_imagem.altura]
        y_max = 0
        left = left_lines[0]
        for line in left_lines:
            _,y = interscetion(line, vertical_esquerda)
            if y > y_max:
                y_max = y
                left = line
        [x1, y1, x2, y2] = left
        cv2.line(objeto_imagem.img, (x1,y1), (x2,y2), (0,0,255), 2)

    cv2.imwrite("./tests/bordas_laterais.jpg", objeto_imagem.img)
    if ha_reta_na_direita == False and ha_reta_na_esquerda == False:
        return [],[],NAO_HA_RETA
    if ha_reta_na_direita == True and ha_reta_na_esquerda == True:
        return left, right, HA_DUAS_RETAS
    if ha_reta_na_direita == False and ha_reta_na_esquerda == True:
        return left, [], SO_ESQUERDA
    if ha_reta_na_direita == True and ha_reta_na_esquerda == False:
        return [], right, SO_DIREITA



def checar_alinhamento_pista_v2(objeto_imagem):
    left, right, caso = bordas_laterais_v2(objeto_imagem)
    k = objeto_imagem.largura//2
    if caso == SO_DIREITA:
        horizontal = [0, objeto_imagem.topo_da_pista, objeto_imagem.largura, objeto_imagem.topo_da_pista]
        x, _ = interscetion(horizontal, right)
        delta_x = x-objeto_imagem.largura//2
        min_largura = int(k - (objeto_imagem.altura - objeto_imagem.topo_da_pista) / coef_angular(right))
        objeto_imagem.img = cv2.circle(objeto_imagem.img, (x, objeto_imagem.topo_da_pista), radius=10, color=(0, 0, 255), thickness=-1)
        objeto_imagem.img = cv2.line(objeto_imagem.img, (objeto_imagem.largura//2 + min_largura, 0), (objeto_imagem.largura//2 + min_largura, objeto_imagem.altura), (127, 127, 0), 2)
        objeto_imagem.img = cv2.line(objeto_imagem.img, (objeto_imagem.largura//2, 0), (objeto_imagem.largura//2, objeto_imagem.altura), (255, 0, 0), 2)
        if delta_x > min_largura and delta_x > 0:
            cv2.putText(objeto_imagem.img,'SO DIREITA: ALINHADO', bottomLeftCornerOfText, font, fontScale, fontColor, lineType)
            return ANDAR
        else:
            cv2.putText(objeto_imagem.img,'SO DIREITA: GIRAR ESQUERDA', bottomLeftCornerOfText, font, fontScale, fontColor, lineType)
            return GIRAR_ESQUERDA
    elif caso == SO_ESQUERDA:
        horizontal = [0, objeto_imagem.topo_da_pista, objeto_imagem.largura, objeto_imagem.topo_da_pista]
        x, _ = interscetion(horizontal, left)
        delta_x = -x + objeto_imagem.largura//2
        min_largura = int(k + (objeto_imagem.altura - objeto_imagem.topo_da_pista) / coef_angular(left))
        objeto_imagem.img = cv2.circle(objeto_imagem.img, (x, objeto_imagem.topo_da_pista), radius=10, color=(0, 0, 255), thickness=-1)
        objeto_imagem.img = cv2.line(objeto_imagem.img, (objeto_imagem.largura//2 - min_largura, 0), (objeto_imagem.largura//2 - min_largura, objeto_imagem.altura), (127, 127, 0), 2)
        objeto_imagem.img = cv2.line(objeto_imagem.img, (objeto_imagem.largura//2, 0), (objeto_imagem.largura//2, objeto_imagem.altura), (255, 0, 0), 2)
        if delta_x > min_largura and delta_x > 0:
            cv2.putText(objeto_imagem.img,'SO ESQUERDA: ALINHADO', bottomLeftCornerOfText, font, fontScale, fontColor, lineType)
            return ANDAR
        else:
            cv2.putText(objeto_imagem.img,'SO ESQUERDA: GIRAR DIREITA', bottomLeftCornerOfText, font, fontScale, fontColor, lineType)
            return GIRAR_DIREITA
    elif caso == NAO_HA_RETA:
        cv2.putText(objeto_imagem.img,'NAO HA RETA', bottomLeftCornerOfText, font, fontScale, fontColor, lineType)
        return ANDAR
    else:
        horizontal = [0, objeto_imagem.topo_da_pista, objeto_imagem.largura, objeto_imagem.topo_da_pista]
        x1, _ = interscetion(horizontal, left)
        x2, _ = interscetion(horizontal, right)
        objeto_imagem.largura_pista = abs(x2 - x1)
        
        delta_x = (x1+x2)//2-objeto_imagem.largura//2
        objeto_imagem.img = cv2.line(objeto_imagem.img, (objeto_imagem.largura//2, 0), (objeto_imagem.largura//2, objeto_imagem.altura), (255, 0, 0), 2)
        objeto_imagem.img = cv2.line(objeto_imagem.img, (int(objeto_imagem.largura_pista//2*objeto_imagem.mult_largura_pista)+(x1+x2)//2, 0), (int(objeto_imagem.largura_pista//2*objeto_imagem.mult_largura_pista)+(x1+x2)//2, objeto_imagem.altura), (127, 127, 0), 2)
        objeto_imagem.img = cv2.line(objeto_imagem.img, (-int(objeto_imagem.largura_pista//2*objeto_imagem.mult_largura_pista)+(x1+x2)//2, 0), (-int(objeto_imagem.largura_pista//2*objeto_imagem.mult_largura_pista)+(x1+x2)//2, objeto_imagem.altura), (127, 127, 0), 2)
        objeto_imagem.img = cv2.circle(objeto_imagem.img, (x1, objeto_imagem.topo_da_pista), radius=10, color=(0, 255, 255), thickness=-1)
        objeto_imagem.img = cv2.circle(objeto_imagem.img, (x2, objeto_imagem.topo_da_pista), radius=10, color=(0, 255, 255), thickness=-1)
        objeto_imagem.img = cv2.circle(objeto_imagem.img, ((x1+x2)//2, objeto_imagem.topo_da_pista), radius=10, color=(0, 0, 255), thickness=-1)
        if objeto_imagem.largura_pista//2*objeto_imagem.mult_largura_pista > abs(delta_x):
            cv2.putText(objeto_imagem.img,'2 RETAS: ALINHADO', bottomLeftCornerOfText, font, fontScale, fontColor, lineType)
            return ANDAR
        elif delta_x > 0:
            cv2.putText(objeto_imagem.img,'2 RETAS: GIRAR DIREITA', bottomLeftCornerOfText, font, fontScale, fontColor, lineType)
            return GIRAR_DIREITA
        else:
            cv2.putText(objeto_imagem.img,'2 RETAS: GIRAR ESQUERDA', bottomLeftCornerOfText, font, fontScale, fontColor, lineType)
            return GIRAR_ESQUERDA

'''Decide para onde virar quando encontra um obstaculo. Recebe somente a camera. Usado apenas no loop de obstaculo.'''
def decisao_desvio(camera: RaspCamera):
    print("Entrando decisao desvio")
    path = camera.take_photo()
    print("Tirou foto")
    objeto_imagem = Classe_imagem(path)
    print("Fez o objeto_imagem")
    x_min, x_max, y = ponto_medio_borda_inferior(objeto_imagem)
    x = (x_min+x_max)//2
    print("Entrou no bordas laterais")
    #lista_esquerda, lista_direita, j = bordas_laterais_v2(objeto_imagem)
    lista_esquerda, lista_direita, j = bordas_laterais_v2(objeto_imagem)
    print("Saiu do bordas laterais")
    poly_left = [coef_angular(lista_esquerda), coef_linear(lista_esquerda)]
    poly_right = [coef_angular(lista_direita), coef_linear(lista_direita)]
    # j = 1: linha central. j = 2: borda direita. j = 3: borda esquerda. j = 0: nenhuma borda
    pixel_scale = 20.4
    d_min = 40
    x_robot = 0
    if x == 0 and y == 0:
        # Nao detectou obstaculo
      #  cv2.putText(objeto_imagem.img,'NAO HA RETA', bottomLeftCornerOfText, font, fontScale, fontColor, lineType)
        print("NAO HA OBSTACULO: ANDAR")
        return ANDAR
    else:
        if j == HA_DUAS_RETAS:
            poly_inv_left = [1/poly_left[0], -poly_left[1]/poly_left[0]]
            x_linha_left = poly_inv_left[1] + poly_inv_left[0]*y
            poly_inv_right = [1/poly_right[0], -poly_right[1]/poly_right[0]]
            x_linha_right = poly_inv_right[1] + poly_inv_right[0]*y
            d_left = abs(x_min - x_linha_left)/pixel_scale
            d_right = abs(x_max - x_linha_right)/pixel_scale
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
                        #cv2.putText(objeto_imagem.img,'2 RETAS: GIRAR ESQUERDA', bottomLeftCornerOfText, font, fontScale, fontColor, lineType)
                        print("HA DUAS RETAS: GIRAR ESQUERDA")
                        return GIRAR_ESQUERDA
                    else:
                  #      cv2.putText(objeto_imagem.img,'2 RETAS: GIRAR DIREITA', bottomLeftCornerOfText, font, fontScale, fontColor, lineType)
                        print("HA DUAS RETAS: GIRAR DIREITA")
                        return GIRAR_DIREITA
                elif d_left > d_min and d_right <= d_min:
                #    cv2.putText(objeto_imagem.img,'2 RETAS: GIRAR ESQUERDA', bottomLeftCornerOfText, font, fontScale, fontColor, lineType)
                    print("HA DUAS RETAS: GIRAR ESQUERDA")
                    return GIRAR_ESQUERDA
                elif d_left <= d_min and d_right > d_min:
                  #  cv2.putText(objeto_imagem.img,'2 RETAS: GIRAR DIREITA', bottomLeftCornerOfText, font, fontScale, fontColor, lineType)
                    print("HA DUAS RETAS: GIRAR DIREITA")
                    return GIRAR_DIREITA
                else:
                    d = max(d_left, d_right)
                    if d == d_left:
                   #     cv2.putText(objeto_imagem.img,'2 RETAS: GIRAR ESQUERDA', bottomLeftCornerOfText, font, fontScale, fontColor, lineType)
                        print("HA DUAS RETAS: GIRAR ESQUERDA")
                        return GIRAR_ESQUERDA
                    else:
                    #    cv2.putText(objeto_imagem.img,'2 RETAS: GIRAR DIREITA', bottomLeftCornerOfText, font, fontScale, fontColor, lineType)
                        print("HA DUAS RETAS: GIRAR DIREITA")
                        return GIRAR_DIREITA
            if x_robot == 1:
                if d_left < d_min:
                 #   cv2.putText(objeto_imagem.img,'2 RETAS: GIRAR DIREITA', bottomLeftCornerOfText, font, fontScale, fontColor, lineType)
                    print("HA DUAS RETAS: GIRAR DIREITA")
                    return GIRAR_DIREITA
                else:
                 #   cv2.putText(objeto_imagem.img,'2 RETAS: GIRAR ESQUERDA', bottomLeftCornerOfText, font, fontScale, fontColor, lineType)
                    print("HA DUAS RETAS: GIRAR ESQUERDA")
                    return GIRAR_ESQUERDA
            if x_robot == 2:
                if d_right < d_min:
                 #   cv2.putText(objeto_imagem.img,'2 RETAS: GIRAR ESQUERDA', bottomLeftCornerOfText, font, fontScale, fontColor, lineType)
                    print("HA DUAS RETAS: GIRAR ESQUERDA")
                    return GIRAR_ESQUERDA
                else:
                #    cv2.putText(objeto_imagem.img,'2 RETAS: GIRAR DIREITA', bottomLeftCornerOfText, font, fontScale, fontColor, lineType)
                    print("HA DUAS RETAS: GIRAR DIREITA")
                    return GIRAR_DIREITA
        if j == SO_DIREITA:
            poly_inv = [1/poly_right[0], -poly_right[1]/poly_right[0]]
            x_linha = poly_inv[1] + poly_inv[0]*y
           # print("imagem: ", ind, "Dist: ", abs(x_max - x_linha)/pixel_scale )
            if abs(x_max - x_linha) > d_min*pixel_scale:
            #    cv2.putText(objeto_imagem.img,'SO DIREITA: GIRAR DIREITA', bottomLeftCornerOfText, font, fontScale, fontColor, lineType)
                print("SO DIREITA: GIRAR DIREITA")
                return GIRAR_DIREITA
            else:
            #    cv2.putText(objeto_imagem.img,'SO DIREITA: GIRAR ESQUERDA', bottomLeftCornerOfText, font, fontScale, fontColor, lineType)
                print("SO DIREITA: GIRAR ESQUERDA")
                return GIRAR_ESQUERDA
        if j == SO_ESQUERDA:
            poly_inv = [1/poly_left[0], -poly_left[1]/poly_left[0]]
            x_linha = poly_inv[1] + poly_inv[0]*y
            #print("imagem: ", ind, "Dist: ", abs(x_min - x_linha)/pixel_scale )
            if abs(x_min - x_linha) > d_min*pixel_scale:
             #   cv2.putText(objeto_imagem.img,'SO ESQUERDA: GIRAR ESQUERDA', bottomLeftCornerOfText, font, fontScale, fontColor, lineType)
                print("SO ESQUERDA: GIRAR ESQUERDA")
                return GIRAR_ESQUERDA
            else:
              #  cv2.putText(objeto_imagem.img,'SO ESQUERDA: GIRAR DIREITA', bottomLeftCornerOfText, font, fontScale, fontColor, lineType)
                print("SO ESQUERDA: GIRAR DIREITA")
                return GIRAR_DIREITA
        if j == NAO_HA_RETA: return ANDAR
