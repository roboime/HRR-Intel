#import sys
#sys.path.insert(1, '../')
from os import listdir
from os.path import  join
from visao import *

path = "./tests/fotos/"

IMAGES = [Classe_imagem(join(path, f)) for f in listdir(join(path))]

ANDAR = "0"                 
GIRAR_ESQUERDA = "1"        
GIRAR_DIREITA = "2"         
PARAR = "3"
SUBIR = "4"
DESCER = "5"


def bordas_laterais_v3(objeto_imagem):
    mask = objeto_imagem.mask("ranges_branco.txt")
    reconhecer_pista(mask, objeto_imagem)
    img = objeto_imagem.img
    edges = cv2.Canny(mask, 50, 150, apertureSize=3)
    #cv2.imwrite("edges_mask.png", edges)

    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength=10, maxLineGap=150)
    coordleft = []
    coordright =[]
   # todas_as_linhas = IMG
    if lines is not None:
        for line in lines:
            line = line.reshape(4)
            x1,y1,x2,y2 = line
         #   img = cv2.line(img, (x1,y1), (x2,y2), (0,127,255), 2)
        
            theta = np.pi/180*RANGE_INCLINACAO
            if y1>objeto_imagem.topo_da_pista and x1 > objeto_imagem.meio_da_pista or y2>objeto_imagem.topo_da_pista and x2 > objeto_imagem.meio_da_pista:
                if math.atan(1)-theta/2 < math.atan(coef_angular(line)) < math.atan(1)+theta/2:
                    coordright.append([x1,y1,x2,y2])
                #    print("angulo : ", 180/np.pi*math.atan(coef_angular(line)))
                  #  print([x1, y1, x2, y2])
                 #   cv2.line(objeto_imagem.img, (x1,y1), (x2,y2), (0,255,0), 2)
            if y1>objeto_imagem.topo_da_pista and x1 < objeto_imagem.meio_da_pista or y2>objeto_imagem.topo_da_pista and x2 < objeto_imagem.meio_da_pista:
                if math.atan(-1)-theta/2 < math.atan(coef_angular(line)) < math.atan(-1)+theta/2:
                    coordleft.append([x1,y1,x2,y2])
                 #   cv2.line(objeto_imagem.img, (x1,y1), (x2,y2), (0,127,0), 2)
    else: return [],[],NAO_HA_RETA
    ha_reta_na_direita = False
   # cv2.imwrite("todas_as_linhas.png", todas_as_linhas)
    if(len(coordright) != 0):
        ha_reta_na_direita = True
        coordright=np.array(coordright)
        mediaright = np.mean(coordright,axis=0)
        lista_media_direita = mediaright.tolist()
        mediaright=mediaright.astype(np.int64)
        [x1,y1,x2,y2]=mediaright
      #  cv2.line(objeto_imagem.img, (x1,y1), (x2,y2), (0,0,255), 2)
        
    ha_reta_na_esquerda = False

    if(len(coordleft) != 0):
        ha_reta_na_esquerda = True
        coordleft=np.array(coordleft)
        medialeft = np.mean(coordleft,axis=0)
        lista_media_esquerda = medialeft.tolist()
        medialeft=medialeft.astype(np.int64)
        [x1,y1,x2,y2]=medialeft
      #  cv2.line(objeto_imagem.img, (x1,y1), (x2,y2), (0,0,255), 2)
        #text= 'y_direita = '+str((y2-y1)/(x2-x1))+' *x + ' +str(y1-(((y2-y1)*x1)/(x2-x1)))
        #img = cv2.putText(img, text, (int(((x1+x2)/2))-450,int(((y1+y2)/2))), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1, cv2.LINE_AA)

    if ha_reta_na_direita == False and ha_reta_na_esquerda == False:
        return [],[],NAO_HA_RETA
    if ha_reta_na_direita == True and ha_reta_na_esquerda == True:
        return lista_media_esquerda, lista_media_direita, HA_DUAS_RETAS
    if ha_reta_na_direita == False and ha_reta_na_esquerda == True:
       return lista_media_esquerda, [], SO_ESQUERDA
    if ha_reta_na_direita == True and ha_reta_na_esquerda == False:
       return [], lista_media_direita, SO_DIREITA

def checar_alinhamento_pista_v2(objeto_imagem):
    left, right, caso = bordas_laterais_v3(objeto_imagem)
    k = objeto_imagem.largura//2
    print("caso == ", caso)
    if caso == SO_DIREITA:
        horizontal = [0, objeto_imagem.topo_da_pista, objeto_imagem.largura, objeto_imagem.topo_da_pista]
        x, _ = interscetion(horizontal, right)
        delta_x = x-objeto_imagem.largura//2
        min_largura = int(k - (objeto_imagem.altura - objeto_imagem.topo_da_pista) / coef_angular(right))
        objeto_imagem.img = cv2.circle(objeto_imagem.img, (x, objeto_imagem.topo_da_pista), radius=10, color=(0, 0, 255), thickness=-1)
        objeto_imagem.img = cv2.line(objeto_imagem.img, (objeto_imagem.largura//2 + min_largura, 0), (objeto_imagem.largura//2 + min_largura, objeto_imagem.altura), (127, 127, 0), 2)
        objeto_imagem.img = cv2.line(objeto_imagem.img, (objeto_imagem.largura//2, 0), (objeto_imagem.largura//2, objeto_imagem.altura), (255, 0, 0), 2)
        if delta_x > min_largura and delta_x > 0:
            print("ALINHADO")
            return ANDAR
        else:
            return GIRAR_ESQUERDA
    elif caso == SO_ESQUERDA:
        horizontal = [0, objeto_imagem.topo_da_pista, objeto_imagem.largura, objeto_imagem.topo_da_pista]
        x, _ = interscetion(horizontal, left)
        delta_x = -x + objeto_imagem.largura//2
        min_largura = int(k + (objeto_imagem.altura - objeto_imagem.topo_da_pista) / coef_angular(left))
        objeto_imagem.img = cv2.circle(objeto_imagem.img, (x, objeto_imagem.topo_da_pista), radius=10, color=(0, 0, 255), thickness=-1)
        objeto_imagem.img = cv2.line(objeto_imagem.img, (objeto_imagem.largura//2 + min_largura, 0), (objeto_imagem.largura//2 + min_largura, objeto_imagem.altura), (127, 127, 0), 2)
        objeto_imagem.img = cv2.line(objeto_imagem.img, (objeto_imagem.largura//2, 0), (objeto_imagem.largura//2, objeto_imagem.altura), (255, 0, 0), 2)
        if delta_x > min_largura and delta_x > 0:
            print("ALINHADO")
            return ANDAR
        else:
            return GIRAR_DIREITA
    elif caso == NAO_HA_RETA:
        print("NAO HA RETA")
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
            print("ALINHADO")
            return ANDAR
        elif delta_x > 0:
            return GIRAR_DIREITA
        else:
            return GIRAR_ESQUERDA
i=1
for IMG in IMAGES:
    ret = checar_alinhamento_pista_v2(IMG)
    if ret == GIRAR_DIREITA:
        print("desalinhado: girar direita")
    if ret == GIRAR_ESQUERDA:
        print("desalinhado: girar esquerda")
    if ret == ANDAR:
        print("Andando")
    cv2.imwrite( path+"../finais/"+str(i)+".png", IMG.img)
    i+=1
    

