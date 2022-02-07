#import sys
#sys.path.insert(1, '../')
from os import listdir
from os.path import  join
from visao import *
from constantes import *

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

def bordas_laterais_v3(objeto_imagem):
    mask = objeto_imagem.mask("ranges_preto.txt")
   # reconhecer_pista(mask, objeto_imagem)
    img = objeto_imagem.img
    edges = cv2.Canny(mask, 50, 150, apertureSize=3)
    cv2.imwrite( path+"../masks/"+str(i)+".png", mask)

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
                   # cv2.line(objeto_imagem.img, (x1,y1), (x2,y2), (0,255,0), 2)
            if y1>objeto_imagem.topo_da_pista or y2>objeto_imagem.topo_da_pista:
                if math.atan(-1)-theta/2 < math.atan(coef_angular(line)) < math.atan(-1)+theta/2:
                    left_lines.append([x1,y1,x2,y2])
               #     cv2.line(objeto_imagem.img, (x1,y1), (x2,y2), (0,127,0), 2)
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

def checar_alinhamento_pista_v1(objeto_imagem, tolerancia_central, tolerancia_para_frente):
 #   path = camera.Take_photo()
  #  objeto_imagem = Classe_imagem(path)
    reta_esquerda, reta_direita, caso = bordas_laterais_v2(objeto_imagem)
    largura, altura = objeto_imagem.largura, objeto_imagem.altura

    print("Estamos no seguinte caso:", caso)
    if(caso == HA_DUAS_RETAS):
        x_intersecao = (coef_linear(reta_direita)-coef_linear(reta_esquerda))/(coef_angular(reta_esquerda)-coef_angular(reta_direita)) 
        '''cv2.circle(img, (int(x_intersecao) , int(coef_angular(reta_direita)*x_intersecao+coef_linear(reta_direita))) , 10,(100,100) , -1)
        cv2.line(img, (reta_direita[X1], reta_direita[Y1]), (reta_direita[X2], reta_direita[Y2]), (0,0,255), 2)
        cv2.line(img, (reta_esquerda[X1], reta_esquerda[Y1]), (reta_esquerda[X2], reta_esquerda[Y2]), (0,0,255), 2)    
        cv2.imshow("na main as DUAS e o PONTO", img)
        cv2.waitKey(0)'''
        proximidade_do_meio = abs((x_intersecao - (largura/2))*100/largura)
        print(proximidade_do_meio)
        if(proximidade_do_meio < tolerancia_central):
            cv2.putText(objeto_imagem.img,'2 RETAS: ALINHADO', bottomLeftCornerOfText, font, fontScale, fontColor, lineType)
            return(ANDAR)
        elif x_intersecao < (largura/2):
            cv2.putText(objeto_imagem.img,'2 RETAS: GIRAR ESQUERDA', bottomLeftCornerOfText, font, fontScale, fontColor, lineType)
            return(GIRAR_ESQUERDA)
        else:
            print("2 RETAS: GIRAR_DIREITA")
            return(GIRAR_DIREITA)

    elif(caso == SO_DIREITA):
        
        #cv2.circle(img, (largura//2 , altura) , 50,(100,100) , -1)
        projecao_na_reta = coef_angular(reta_direita)*(largura/2) + coef_linear(reta_direita)
        '''cv2.line(img, (reta_direita[X1], reta_direita[Y1]), (reta_direita[X2], reta_direita[Y2]), (0,0,255), 2)
        cv2.circle(img, (largura//2 , int(projecao_na_reta)) , 10,(100,100) , -1)
        cv2.imshow("so direita", img)
        cv2.waitKey(0)'''
        if ((altura-projecao_na_reta)*100 / altura) > tolerancia_para_frente:
            cv2.putText(objeto_imagem.img,'SO DIREITA: ALINHADO', bottomLeftCornerOfText, font, fontScale, fontColor, lineType)
            return(ANDAR)
        else:
            cv2.putText(objeto_imagem.img,'SO DIREITA: GIRAR ESQUERDA', bottomLeftCornerOfText, font, fontScale, fontColor, lineType)
            return(GIRAR_ESQUERDA)

    elif(caso == SO_ESQUERDA):
        #cv2.circle(img, (largura//2 , altura) , 50,(100,100) , -1)
        projecao_na_reta = coef_angular(reta_esquerda)*(largura/2) + coef_linear(reta_esquerda)
        '''cv2.line(img, (reta_esquerda[X1], reta_esquerda[Y1]), (reta_esquerda[X2], reta_esquerda[Y2]), (0,0,255), 2)
        cv2.circle(img, (largura//2 , int(projecao_na_reta)) , 10,(100,100) , -1)
        cv2.imshow("so esquerda", img)
        cv2.waitKey(0)'''
        if ((altura-projecao_na_reta)*100 / altura) > tolerancia_para_frente:
            cv2.putText(objeto_imagem.img,'SO ESQUERDA: ALINHADO', bottomLeftCornerOfText, font, fontScale, fontColor, lineType)
            return(ANDAR)
        else:
            cv2.putText(objeto_imagem.img,'SO ESQUERDA: GIRAR DIREITA', bottomLeftCornerOfText, font, fontScale, fontColor, lineType)
            return(GIRAR_DIREITA)

    else:
        cv2.putText(objeto_imagem.img,'NAO HA RETA', bottomLeftCornerOfText, font, fontScale, fontColor, lineType)
        return(ANDAR)

'''
    Funcao que retorna ANDAR, caso o robo esteja alinhado com a pista, e GIRAR_ESQUERDA ou GIRAR_DIREITA, caso contrario.
    Recebe objeto relativo a Classe_camera(), tira a foto e obtem dela as bordas laterais.
    Em seuida analisa-se os casos:
    NAO_HA_RETA - Acontecera quando o robo estiver muito proximo da linha de chegada, entao retorna ANDAR.
    SO_DIREITA ou SO_ESQUERDA - Calcula-se a interseccao (x, y) da borda com o topo_da_pista. Se a borda nao cortar o meio da imagem
    e (x - largura)//2  for maior que min_largura, que calculado eh usando a geometria da imagem, entao a direcao esta certa. Senao,
    retornara para girar.
    HA_DUAS_RETAS - Neste caso, calcula-se a interseccao das duas bordas com o topo da pista. Se o meio da imagem estiver entre os 2 pontos
    e numa folga relativa a largura do robo, entao o robo esta na direcao certa. Senao, retornara para girar.
'''


def checar_alinhamento_pista_v2(objeto_imagem):
    left, right, caso = bordas_laterais_v3(objeto_imagem)
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
i=1
for IMG in IMAGES:
    ret = checar_alinhamento_pista_v2(IMG)
    cv2.imwrite( path+"../finais/"+str(i)+".png", IMG.img)
    i+=1