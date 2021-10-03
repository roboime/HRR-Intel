#import pickle
import time
import numpy as np
import cv2
import visao

ANDAR = "0"                 
GIRAR_ESQUERDA = "1"        
GIRAR_DIREITA = "2"         
PARAR = "3"
SUBIR = "4"
DESCER = "5"

ANG_GIRADO = 0.0
ANG_CABECA_OBSTACULO = 0.0
ANG_CABECA_DEGRAU = 0.0
DIST_MIN_OBST_ATUAL = 46.0

# Utiliza giroscopio, a principio nao vai ser utilizado
#peguei o giroscopio pois imaginei que o robo poderia precisar fazer alguma correcao 
# durante a trajetoria futuramente
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



# Essa funcao roda até o robô estar alinhado com a pista
# O alinhamento é medido pela função "esta_alinhado()"
# Falta implementar a funcao 'esta_alinhado()'
def quando_parar_de_alinhar(angulo_erro_max, s_giroscopio):
    while (not esta_alinhado(angulo_erro_max)):
        continue
    return PARAR



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


def decisao_desvio(camera):
    x, y = ponto_medio_borda_inferior(camera.Take_photo())
    poly_left, poly_right, j = visao.bordas_laterais()

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

def quando_parar_de_girar(sensor_distancia, vel_ang, largura_robo):
    global DIST_MIN_OBST_ATUAL
    global ANG_GIRADO_VEL_ANG
    global ANG_GIRADO_TRIGO
    tempo1 = tempo2 = time.time()
    while (tempo2 - tempo1 < 5):
        print(sensor_distancia.Get_distance())
        tempo2 = time.time()
    
    intervalo_medicoes = 0.2
    mult_dist = 1
    mult_largura = 0.75
    DIST_MIN_OBST_ATUAL = sensor_distancia.Get_distance()
    
    t_0 = t_1 = time.time()
    while True:
        time.sleep(intervalo_medicoes)
        sensor_distancia.Get_distance()
        if(abs(sensor_distancia.atual - sensor_distancia.anterior) > mult_dist*sensor_distancia.anterior):    
            t_1 = time.time() - intervalo_medicoes/2
            theta_vel_ang = vel_ang*(t_1 - t_0)
            theta_trigo = np.arccos(DIST_MIN_OBST_ATUAL/sensor_distancia.anterior)
            ANG_GIRADO_VEL_ANG = np.arctan2( DIST_MIN_OBST_ATUAL*np.tan(theta_vel_ang) + largura_robo*mult_largura, DIST_MIN_OBST_ATUAL)
            ANG_GIRADO_TRIGO = np.arctan2( DIST_MIN_OBST_ATUAL*np.tan(theta_trigo) + largura_robo*mult_largura, DIST_MIN_OBST_ATUAL)
            print("ANG_GIRADO_VEL_ANG: ", ANG_GIRADO_VEL_ANG, "\nANG_GIRADO_TRIGO: ", ANG_GIRADO_TRIGO, "\n")
            break;

    print("Saimo familia")

    return PARAR