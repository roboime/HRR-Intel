#import sys
#sys.path.insert(1, '../')
from os import listdir
from os.path import  join
from visao import *
import copy

path = "./tests/fotos_main/"

IMAGES = [Classe_imagem(join(path, f)) for f in listdir(join(path))]

ANDAR = "0"                 
GIRAR_ESQUERDA = "1"        
GIRAR_DIREITA = "2"         
PARAR = "3"
SUBIR = "4"
DESCER = "5"


font                   = cv2.FONT_HERSHEY_SIMPLEX
bottomLeftCornerOfText = (10,500)
fontScale              = 1
fontColor              = (255,255,255)
lineType               = 2

def ponto_medio_borda_inferior2(objeto_imagem):
    
    orangemask = objeto_imagem.mask("ranges_laranja.txt")
    cv2.imwrite( path+"../masks/"+str(ind)+".png", orangemask)
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
    segmentos = cv2.HoughLinesP(lista_bordas, rho=1, theta=np.pi/180, threshold=100,
                            lines=np.array([]), minLineLength=minLineLength, maxLineGap=10)
    if segmentos is None: return 0,0, 0
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

    print("Pto_Med_Borda_Inf-Num_seg: {} before for".format(numero_segmentos))
    for i in range(numero_segmentos):
        x1, y1, x2, y2 = segmentos[i].reshape(4)
        cv2.line(objeto_imagem.img, (x1,y1), (x2,y2), (255,0,255), 2)
        if (segmentos[i][0][Y1] > ymed_bloco_todo*fator_para_baixo or segmentos[i][0][Y2] > ymed_bloco_todo*fator_para_baixo):
            x_min = min(x_min, segmentos[i][0][X1], segmentos[i][0][X2])
            x_max = max(x_max, segmentos[i][0][X1], segmentos[i][0][X2])
            y_max = max(y_max, segmentos[i][0][Y1], segmentos[i][0][Y2])
    x_med = (x_min + x_max) // 2
    print("Pto_Med_Borda_Inf-Num_seg: {} after for".format(numero_segmentos))
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
    return x_min, x_max, y_max

def bordas_laterais_v3(objeto_imagem):
    mask = objeto_imagem.mask("ranges_preto.txt")
   # reconhecer_pista(mask, objeto_imagem)
    img = objeto_imagem.img
    edges = cv2.Canny(mask, 50, 150, apertureSize=3)
  #  cv2.imwrite( path+"../masks/"+str(ind)+".png", mask)

    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength=10, maxLineGap=150)
    left_lines = []
    right_lines =[]
   # todas_as_linhas = IMG
    if lines is not None:
        for line in lines:
            line = line.reshape(4)
            x1,y1,x2,y2 = line
            img = cv2.line(img, (x1,y1), (x2,y2), (0,127,255), 2)
        
            theta = np.pi/180*RANGE_INCLINACAO
            if y1>objeto_imagem.topo_da_pista or y2>objeto_imagem.topo_da_pista:
                if math.atan(1)-theta/2 < math.atan(coef_angular(line)) < math.atan(1)+theta/2:
                    right_lines.append([x1,y1,x2,y2])
                #    print("angulo : ", 180/np.pi*math.atan(coef_angular(line)))
                  #  print([x1, y1, x2, y2])
                    cv2.line(objeto_imagem.img, (x1,y1), (x2,y2), (0,255,0), 2)
            if y1>objeto_imagem.topo_da_pista or y2>objeto_imagem.topo_da_pista:
                if math.atan(-1)-theta/2 < math.atan(coef_angular(line)) < math.atan(-1)+theta/2:
                    left_lines.append([x1,y1,x2,y2])
                    cv2.line(objeto_imagem.img, (x1,y1), (x2,y2), (0,127,0), 2)
    else: return [],[],NAO_HA_RETA
   # cv2.imwrite("todas_as_linhas.png", todas_as_linhas)

    ha_reta_na_direita = False
    if(len(right_lines) != 0):
        ha_reta_na_direita = True
        vertical_direita = [objeto_imagem.largura,0,objeto_imagem.largura,objeto_imagem.altura]
        y_max = 0
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
        for line in left_lines:
            _,y = interscetion(line, vertical_esquerda)
            if y > y_max:
                y_max = y
                left = line
        [x1, y1, x2, y2] = left
        cv2.line(objeto_imagem.img, (x1,y1), (x2,y2), (0,0,255), 2)
    
    if ha_reta_na_direita == False and ha_reta_na_esquerda == False:
        return [],[],NAO_HA_RETA
    if ha_reta_na_direita == True and ha_reta_na_esquerda == True:
        return left, right, HA_DUAS_RETAS
    if ha_reta_na_direita == False and ha_reta_na_esquerda == True:
       return left, [], SO_ESQUERDA
    if ha_reta_na_direita == True and ha_reta_na_esquerda == False:
       return [], right, SO_DIREITA

def decisao_desvio2(objeto_imagem):
  #  path = camera.Take_photo()
    #objeto_imagem = Classe_imagem(path)
    x_min, x_max, y = ponto_medio_borda_inferior2(objeto_imagem)
    x = (x_min+x_max)//2
    lista_esquerda, lista_direita, j = bordas_laterais_v3(objeto_imagem)
    poly_left = [coef_angular(lista_esquerda), coef_linear(lista_esquerda)]
    poly_right = [coef_angular(lista_direita), coef_linear(lista_direita)]
    # j = 1: linha central. j = 2: borda direita. j = 3: borda esquerda. j = 0: nenhuma borda
    pixel_scale = 20.4
    d_min = 40
    x_robot = 0
    if x == 0 and y == 0:
        # Nao detectou obstaculo
        cv2.putText(objeto_imagem.img,'NAO HA RETA', bottomLeftCornerOfText, font, fontScale, fontColor, lineType)
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
                        cv2.putText(objeto_imagem.img,'2 RETAS: GIRAR ESQUERDA', bottomLeftCornerOfText, font, fontScale, fontColor, lineType)
                        return GIRAR_ESQUERDA
                    else:
                        cv2.putText(objeto_imagem.img,'2 RETAS: GIRAR DIREITA', bottomLeftCornerOfText, font, fontScale, fontColor, lineType)
                        return GIRAR_DIREITA
                elif d_left > d_min and d_right <= d_min:
                    cv2.putText(objeto_imagem.img,'2 RETAS: GIRAR ESQUERDA', bottomLeftCornerOfText, font, fontScale, fontColor, lineType)
                    return GIRAR_ESQUERDA
                elif d_left <= d_min and d_right > d_min:
                    cv2.putText(objeto_imagem.img,'2 RETAS: GIRAR DIREITA', bottomLeftCornerOfText, font, fontScale, fontColor, lineType)
                    return GIRAR_DIREITA
                else:
                    d = max(d_left, d_right)
                    if d == d_left:
                        cv2.putText(objeto_imagem.img,'2 RETAS: GIRAR ESQUERDA', bottomLeftCornerOfText, font, fontScale, fontColor, lineType)
                        return GIRAR_ESQUERDA
                    else:
                        cv2.putText(objeto_imagem.img,'2 RETAS: GIRAR DIREITA', bottomLeftCornerOfText, font, fontScale, fontColor, lineType)
                        return GIRAR_DIREITA
            if x_robot == 1:
                if d_left < d_min:
                    cv2.putText(objeto_imagem.img,'2 RETAS: GIRAR DIREITA', bottomLeftCornerOfText, font, fontScale, fontColor, lineType)
                    return GIRAR_DIREITA
                else:
                    cv2.putText(objeto_imagem.img,'2 RETAS: GIRAR ESQUERDA', bottomLeftCornerOfText, font, fontScale, fontColor, lineType)
                    return GIRAR_ESQUERDA
            if x_robot == 2:
                if d_right < d_min:
                    cv2.putText(objeto_imagem.img,'2 RETAS: GIRAR ESQUERDA', bottomLeftCornerOfText, font, fontScale, fontColor, lineType)
                    return GIRAR_ESQUERDA
                else:
                    cv2.putText(objeto_imagem.img,'2 RETAS: GIRAR DIREITA', bottomLeftCornerOfText, font, fontScale, fontColor, lineType)
                    return GIRAR_DIREITA
        if j == SO_DIREITA:
            poly_inv = [1/poly_right[0], -poly_right[1]/poly_right[0]]
            x_linha = poly_inv[1] + poly_inv[0]*y
            print("imagem: ", ind, "Dist: ", abs(x_max - x_linha)/pixel_scale )
            if abs(x_max - x_linha) > d_min*pixel_scale:
                cv2.putText(objeto_imagem.img,'SO DIREITA: GIRAR DIREITA', bottomLeftCornerOfText, font, fontScale, fontColor, lineType)
                return GIRAR_DIREITA
            else:
                cv2.putText(objeto_imagem.img,'SO DIREITA: GIRAR ESQUERDA', bottomLeftCornerOfText, font, fontScale, fontColor, lineType)
                return GIRAR_ESQUERDA
        if j == SO_ESQUERDA:
            poly_inv = [1/poly_left[0], -poly_left[1]/poly_left[0]]
            x_linha = poly_inv[1] + poly_inv[0]*y
            print("imagem: ", ind, "Dist: ", abs(x_min - x_linha)/pixel_scale )
            if abs(x_min - x_linha) > d_min*pixel_scale:
                cv2.putText(objeto_imagem.img,'SO ESQUERDA: GIRAR ESQUERDA', bottomLeftCornerOfText, font, fontScale, fontColor, lineType)
                return GIRAR_ESQUERDA
            else:
                cv2.putText(objeto_imagem.img,'SO ESQUERDA: GIRAR DIREITA', bottomLeftCornerOfText, font, fontScale, fontColor, lineType)
                return GIRAR_DIREITA
        if j == NAO_HA_RETA: return ANDAR

ind=1
for IMG in IMAGES:
    i1 = copy.copy(IMG)
    i2 = copy.copy(IMG)
    ret = decisao_desvio2(IMG)
    cv2.imwrite( path+"../finais2/"+str(ind)+".png", IMG.img)
  #  ret = checar_alinhamento_pista_v2(i2)
   # cv2.imwrite( path+"../finais/"+str(i)+".png", IMG.img)
    ind+=1