#import pickle
import time
import numpy as np
import cv2
from visao import *
import PiCamera as picamera
import classes


X1 = 0
Y1 = 1
X2 = 2
Y2 = 3

ANDAR = "0"                 
GIRAR_ESQUERDA = "1"        
GIRAR_DIREITA = "2"         
PARAR = "3"
SUBIR = "4"
DESCER = "5"

NAO_HA_RETA = 0
HA_DUAS_RETAS = 1
SO_ESQUERDA = 2
SO_DIREITA = 3
casos_dic = ["NAO_HA_RETA", "HA_DUAS_RETAS", "SO_ESQUERDA", "SO_DIREITA"]

ANG_GIRADO = 0.0
ANG_CABECA_OBSTACULO = 0.0
ANG_CABECA_DEGRAU = 0.0
DIST_MIN_OBST_ATUAL = 46.0

# Utiliza giroscopio, a principio nao vai ser utilizado
#peguei o giroscopio pois imaginei que o robo poderia precisar fazer alguma correcao 
# durante a trajetoria futuramente

def quando_parar_de_girar(sensor_distancia, vel_ang, largura_robo):
    global DIST_MIN_OBST_ATUAL
    global ANG_GIRADO
    
    intervalo_medicoes = 0.1
    mult_dist = 1.0
    mult_largura = 0.75
    mult_ang_girado = 0.5
    DIST_MIN_OBST_ATUAL = sensor_distancia.Get_distance()
    
    t_0 = t_1 = time.time()
    while True:
        time.sleep(intervalo_medicoes)
        sensor_distancia.Get_distance()
        if sensor_distancia.atual < sensor_distancia.anterior:
            DIST_MIN_OBST_ATUAL = sensor_distancia.atual
            t_0 = t_1
        if(abs(sensor_distancia.atual - sensor_distancia.anterior) > mult_dist*sensor_distancia.anterior):    
            t_1 = time.time() - intervalo_medicoes/2
            theta_vel_ang = vel_ang*(t_1 - t_0)
            theta_trigo = np.arccos(DIST_MIN_OBST_ATUAL/sensor_distancia.anterior)
            ANG_GIRADO_VEL_ANG = np.arctan2( DIST_MIN_OBST_ATUAL*np.tan(theta_vel_ang) + largura_robo*mult_largura, DIST_MIN_OBST_ATUAL)
            ANG_GIRADO_TRIGO = np.arctan2( DIST_MIN_OBST_ATUAL*np.tan(theta_trigo) + largura_robo*mult_largura, DIST_MIN_OBST_ATUAL)
        #    print("ANG_GIRADO_VEL_ANG: ", ANG_GIRADO_VEL_ANG, "\nANG_GIRADO_TRIGO: ", ANG_GIRADO_TRIGO, "\n")
            ANG_GIRADO = mult_ang_girado*ANG_GIRADO_TRIGO + (1-mult_ang_girado)*ANG_GIRADO_VEL_ANG
            intervalo_seguranca = ANG_GIRADO/vel_ang - (t_1 - t_0)
            time.sleep(intervalo_seguranca)
            break

  #  print("Saimo familia")
    return PARAR

def quando_parar_de_andar_giroscopio(giroscopio, s_distancia, velocidade, largura_do_robo):
    projecao_horizontal_trajetoria = s_distancia.anterior*np.cos(np.pi/180 * giroscopio.Obter_angulo_yaw()) + largura_do_robo
    projecao_vertical_trajetoria = s_distancia.anterior*np.sin(np.pi/180 * giroscopio.Obter_angulo_yaw())

    trajetoria = ( projecao_vertical_trajetoria**2 +projecao_horizontal_trajetoria**2 ) ** (1/2)
    tempo_necessario = trajetoria/velocidade
    instante_inicial = time.time()

    while (time.time() - instante_inicial < tempo_necessario):
        print("andamos ", velocidade*time.time() - instante_inicial(), " de ", trajetoria)

    return PARAR



# Utiliza somente a camera e o sensor de distancia
# Deixa o robo andando durante o tempo necessario
def quando_parar_de_andar_visaocomp(velocidade):
    instante_inicial = time.time()

    dist_estimado = (DIST_MIN_OBST_ATUAL*np.cos(ANG_CABECA_OBSTACULO)) / np.cos(ANG_GIRADO)
    tempo_estimado = dist_estimado / velocidade

    while (time.time() - instante_inicial < tempo_estimado):
        continue

    return PARAR

def decisao_desvio(camera):
    camera.Take_photo()
    objeto_imagem = classes.Classe_imagem(camera.image_path)
    x, y = ponto_medio_borda_inferior(objeto_imagem)
    lista_esquerda, lista_direita, j = bordas_laterais_v2(objeto_imagem)
    poly_left = [coef_angular(lista_esquerda), coef_linear(lista_esquerda)]
    poly_right = [coef_angular(lista_direita), coef_linear(lista_direita)]
    # j = 1: linha central. j = 2: borda direita. j = 3: borda esquerda. j = 0: nenhuma borda
    pixel_scale = 20.4
    d_min = 40
    x_robot = 0
    if x == 0 and y == 0:
        # Não detectou obstáculo
        return ANDAR
    else:
        if j == 1:
            poly_inv_left = [1/poly_left[0], -poly_left[1]/poly_left[0]]
            x_linha_left = poly_inv_left[1] + poly_inv_left[0]*y
            poly_inv_right = [1/poly_right[0], -poly_right[1]/poly_right[0]]
            x_linha_right = poly_inv_right[1] + poly_inv_right[0]*y
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
                        return GIRAR_ESQUERDA
                    else:
                        return GIRAR_DIREITA
                elif d_left > d_min and d_right <= d_min:
                    return GIRAR_ESQUERDA
                elif d_left <= d_min and d_right > d_min:
                    return GIRAR_DIREITA
                else:
                    d = max(d_left, d_right)
                    if d == d_left:
                        return GIRAR_ESQUERDA
                    else:
                        return GIRAR_DIREITA
            if x_robot == 1:
                if d_left < d_min:
                    return GIRAR_DIREITA
                else:
                    return GIRAR_ESQUERDA
            if x_robot == 2:
                if d_right < d_min:
                    return GIRAR_ESQUERDA
                else:
                    return GIRAR_DIREITA
        if j == 2:
            poly_inv = [1/poly_right[0], -poly_right[1]/poly_right[0]]
            x_linha = poly_inv[1] + poly_inv[0]*y
            if abs(x - x_linha) > d_min*pixel_scale:
                return GIRAR_DIREITA
            else:
                return GIRAR_ESQUERDA
        if j == 3:
            poly_inv = [1/poly_left[0], -poly_left[1]/poly_left[0]]
            x_linha = poly_inv[1] + poly_inv[0]*y
            if abs(x - x_linha) > d_min*pixel_scale:
                return GIRAR_ESQUERDA
            else:
                return GIRAR_DIREITA
        if j == 0: return ANDAR


def checar_alinhamento_pista_v1(camera, tolerancia_central, tolerancia_para_frente):
    path = camera.Take_photo()
    objeto_imagem = Classe_imagem(path)
    reta_esquerda, reta_direita, caso = bordas_laterais_v1(objeto_imagem)
    largura, altura = objeto_imagem.largura, objeto_imagem.altura

    print("Estamos no seguinte caso:", casos_dic[caso])
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
            print("ANDAR")
            return(ANDAR)
        elif x_intersecao < (largura/2):
            print("GIRAR_ESQUERDA")
            return(GIRAR_ESQUERDA)
        else:
            print("GIRAR_DIREITA")
            return(GIRAR_DIREITA)

    elif(caso == SO_DIREITA):
        
        #cv2.circle(img, (largura//2 , altura) , 50,(100,100) , -1)
        projecao_na_reta = coef_angular(reta_direita)*(largura/2) + coef_linear(reta_direita)
        '''cv2.line(img, (reta_direita[X1], reta_direita[Y1]), (reta_direita[X2], reta_direita[Y2]), (0,0,255), 2)
        cv2.circle(img, (largura//2 , int(projecao_na_reta)) , 10,(100,100) , -1)
        cv2.imshow("so direita", img)
        cv2.waitKey(0)'''
        if ((altura-projecao_na_reta)*100 / altura) > tolerancia_para_frente:
            print("ANDAR")
            return(ANDAR)
        else:
            print("GIRAR_ESQUERDA")
            return(GIRAR_ESQUERDA)

    elif(caso == SO_ESQUERDA):
        #cv2.circle(img, (largura//2 , altura) , 50,(100,100) , -1)
        projecao_na_reta = coef_angular(reta_esquerda)*(largura/2) + coef_linear(reta_esquerda)
        '''cv2.line(img, (reta_esquerda[X1], reta_esquerda[Y1]), (reta_esquerda[X2], reta_esquerda[Y2]), (0,0,255), 2)
        cv2.circle(img, (largura//2 , int(projecao_na_reta)) , 10,(100,100) , -1)
        cv2.imshow("so esquerda", img)
        cv2.waitKey(0)'''
        if ((altura-projecao_na_reta)*100 / altura) > tolerancia_para_frente:
            print("ANDAR")
            return(ANDAR)
        else:
            print("GIRAR_DIREITA")
            return(GIRAR_DIREITA)

    else:
        print("nenhuma reta encontrada, andando em frente")
        return(ANDAR)

def checar_alinhamento_pista_v2(camera):
    path = camera.Take_photo()
    objeto_imagem = Classe_imagem(path)
    left, right, caso = bordas_laterais_v2(objeto_imagem)
    k = objeto_imagem.largura//2
    if caso == SO_DIREITA:
        horizontal = [0, objeto_imagem.topo_da_pista, objeto_imagem.largura, objeto_imagem.topo_da_pista]
        x, _ = interscetion(horizontal, right)
        delta_x = x-objeto_imagem.largura//2
        min_largura = k - (objeto_imagem.altura - objeto_imagem.topo_da_pista) / coef_angular(right)
  #      objeto_imagem.img = cv2.circle(objeto_imagem.img, (x, objeto_imagem.topo_da_pista), radius=10, color=(0, 0, 255), thickness=-1)
   #     objeto_imagem.img = cv2.line(objeto_imagem.img, (objeto_imagem.largura//2 + min_largura, 0), (objeto_imagem.largura//2 + min_largura, objeto_imagem.altura), (127, 127, 0), 2)
    #    objeto_imagem.img = cv2.line(objeto_imagem.img, (objeto_imagem.largura//2, 0), (objeto_imagem.largura//2, objeto_imagem.altura), (255, 0, 0), 2)
        if delta_x > min_largura and delta_x > 0:
            return ANDAR
        else:
            return GIRAR_ESQUERDA
    elif caso == SO_ESQUERDA:
        horizontal = [0, objeto_imagem.topo_da_pista, objeto_imagem.largura, objeto_imagem.topo_da_pista]
        x, _ = interscetion(horizontal, left)
        delta_x = -x + objeto_imagem.largura//2
        min_largura = k + (objeto_imagem.altura - objeto_imagem.topo_da_pista) / coef_angular(left)
        #objeto_imagem.img = cv2.circle(objeto_imagem.img, (x, objeto_imagem.topo_da_pista), radius=10, color=(0, 0, 255), thickness=-1)
        #objeto_imagem.img = cv2.line(objeto_imagem.img, (objeto_imagem.largura//2 + min_largura, 0), (objeto_imagem.largura//2 + min_largura, objeto_imagem.altura), (127, 127, 0), 2)
        #objeto_imagem.img = cv2.line(objeto_imagem.img, (objeto_imagem.largura//2, 0), (objeto_imagem.largura//2, objeto_imagem.altura), (255, 0, 0), 2)
        if delta_x > min_largura and delta_x > 0:
            return ANDAR
        else:
            return GIRAR_DIREITA
    elif caso == NAO_HA_RETA:
        return ANDAR
    else:
        horizontal = [0, objeto_imagem.topo_da_pista, objeto_imagem.largura, objeto_imagem.topo_da_pista]
        x1, _ = interscetion(horizontal, left)
        x2, _ = interscetion(horizontal, right)
        largura_pista = abs(x2 - x1)
        mult_largura_pista = 0.7
        delta_x = (x1+x2)//2-objeto_imagem.largura//2
#        objeto_imagem.img = cv2.line(objeto_imagem.img, (objeto_imagem.largura//2, 0), (objeto_imagem.largura//2, objeto_imagem.altura), (255, 0, 0), 2)
 #       objeto_imagem.img = cv2.line(objeto_imagem.img, (int(objeto_imagem.largura_pista//2*objeto_imagem.mult_largura_pista)+(x1+x2)//2, 0), (int(objeto_imagem.largura_pista//2*objeto_imagem.mult_largura_pista)+(x1+x2)//2, objeto_imagem.altura), (127, 127, 0), 2)
  #      objeto_imagem.img = cv2.line(objeto_imagem.img, (-int(objeto_imagem.largura_pista//2*objeto_imagem.mult_largura_pista)+(x1+x2)//2, 0), (-int(objeto_imagem.largura_pista//2*objeto_imagem.mult_largura_pista)+(x1+x2)//2, objeto_imagem.altura), (127, 127, 0), 2)
   #     objeto_imagem.img = cv2.circle(objeto_imagem.img, (x1, objeto_imagem.topo_da_pista), radius=10, color=(0, 255, 255), thickness=-1)
    #    objeto_imagem.img = cv2.circle(objeto_imagem.img, (x2, objeto_imagem.topo_da_pista), radius=10, color=(0, 255, 255), thickness=-1)
     #   objeto_imagem.img = cv2.circle(objeto_imagem.img, ((x1+x2)//2, objeto_imagem.topo_da_pista), radius=10, color=(0, 0, 255), thickness=-1)
        if largura_pista//2*mult_largura_pista > abs(delta_x):
            return ANDAR
        elif delta_x > 0:
            return GIRAR_DIREITA
        else:
            return GIRAR_ESQUERDA