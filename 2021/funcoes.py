#import pickle
import time
import numpy as np
import cv2
from visao import *
import picamera
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
ANG_PITCH_CABECA = 30.0
ANG_CABECA_DEGRAU = 0.0
DIST_MAXIMA = 50
DIST_MIN_OBST_ATUAL = 50.0


'''Gira o robo ate haver uma variacao brusca de distancia, quando eh suposto nao haver mais obstaculo na direcao, acrescido
de uma margem de segurnca dependente da altura do robo. Usada em Loop Obstaculo'''

def quando_parar_de_girar(sensor_distancia, vel_ang, largura_robo):
    global DIST_MIN_OBST_ATUAL
    global ANG_GIRADO
    
    intervalo_medicoes = 0.2
    mult_dist = 4
    mult_largura = 0.6
    mult_ang_girado = 0
    sensor_distancia.Get_distance()
    sensor_distancia.atual *= np.cos(ANG_PITCH_CABECA*np.pi/180)
    DIST_MIN_OBST_ATUAL = sensor_distancia.atual
    
    t_0 = t_1 = time.time()
    while True:
        time.sleep(intervalo_medicoes)
        sensor_distancia.Get_distance()
        sensor_distancia.atual *= np.cos(ANG_PITCH_CABECA*np.pi/180)
       # print("Dist: ", sensor_distancia.atual)
        if sensor_distancia.atual < sensor_distancia.anterior:
            DIST_MIN_OBST_ATUAL = sensor_distancia.atual
            t_0 = t_1
      #  print("TEMPO: ", t_1-t_0)
        if(sensor_distancia.atual > DIST_MAXIMA):    
            t_1 = time.time() - intervalo_medicoes/2
            theta_vel_ang = vel_ang*(t_1 - t_0)
            #theta_trigo = np.arccos(DIST_MIN_OBST_ATUAL/sensor_distancia.anterior)
            ANG_GIRADO = np.arctan2( DIST_MIN_OBST_ATUAL*np.tan(theta_vel_ang) + largura_robo*mult_largura, DIST_MIN_OBST_ATUAL)
           # ANG_GIRADO_TRIGO = np.arctan2( DIST_MIN_OBST_ATUAL*np.tan(theta_trigo) + largura_robo*mult_largura, DIST_MIN_OBST_ATUAL)
        #    print("ANG_GIRADO_VEL_ANG: ", ANG_GIRADO_VEL_ANG, "\nANG_GIRADO_TRIGO: ", ANG_GIRADO_TRIGO, "\n")
           # ANG_GIRADO = mult_ang_girado*ANG_GIRADO_TRIGO + (1-mult_ang_girado)*ANG_GIRADO_VEL_ANG
            intervalo_seguranca = ANG_GIRADO/vel_ang - (t_1 - t_0)
            time.sleep(intervalo_seguranca)
            break
        t_1 = time.time()
 #   print("ANG GIRADO: ", ANG_GIRADO)
    return PARAR

def quando_parar_de_realinhar(vel_ang, sentido_de_giro):
    global ANG_GIRADO
    intervalo_realinhamento = ANG_GIRADO/vel_ang
    intervalo_medicoes = 0.2
    t_0 = t_1 = time.time()
    while True:
        time.sleep(intervalo_medicoes)
        t_1 = time.time()
        if t_1-t_0 > intervalo_realinhamento: 
            break
        if(sentido_de_giro == GIRAR_DIREITA):
            print("girando para a  DIREITA, faltam ", ANG_GIRADO- vel_ang * (t_1-t_0), "radianos para compensar o angulo girado")
        else:
            print("girando para a  ESQUERDA, faltam ", ANG_GIRADO- vel_ang * (t_1-t_0), "radianos para compensar o angulo girado")

    return ANDAR
'''
Funcao que seria usada no loop de obstaculo se conseguissemos usar o giroscopio.'''
def quando_parar_de_andar_giroscopio(giroscopio, s_distancia, velocidade, largura_do_robo):
    projecao_horizontal_trajetoria = s_distancia.anterior *np.cos(ANG_PITCH_CABECA*np.pi/180) / np.cos(np.pi/180 * giroscopio.Obter_angulo_yaw()) + largura_do_robo
    projecao_vertical_trajetoria = s_distancia.anterior *np.cos(ANG_PITCH_CABECA*np.pi/180) / np.sin(np.pi/180 * giroscopio.Obter_angulo_yaw())

    trajetoria = ( projecao_vertical_trajetoria**2 +projecao_horizontal_trajetoria**2 ) ** (1/2)
    tempo_necessario = trajetoria/velocidade
    instante_inicial = time.time()

    while (time.time() - instante_inicial < tempo_necessario):
        print("andamos ", velocidade*time.time() - instante_inicial(), " de ", trajetoria)

    return PARAR



'''Utiliza somente a velocidade e a variavel global angular definida pela funcao quando parar de girar'''
def quando_parar_de_andar_visaocomp(velocidade):
    instante_inicial = time.time()

    dist_estimado = (DIST_MIN_OBST_ATUAL*np.cos(ANG_PITCH_CABECA*np.pi/180)) / np.cos(ANG_GIRADO)
    tempo_estimado = dist_estimado / velocidade

    while (time.time() - instante_inicial < tempo_estimado):
        continue

    return PARAR



# No momento nao utilizada em funcao de poder ser feita apenas com whiles dentro do loop
def quando_parar_de_alinhar(tolerancia_centro, tolerancia_para_frente):
    camera = picamera.PiCamera()
    
    while (checar_alinhamento_pista_v1(camera, tolerancia_centro, tolerancia_para_frente) != ANDAR):
        continue

    return PARAR


'''Decide para onde virar quando encontra um obstaculo. Recebe somente a camera. Usado apenas no loop de obstaculo.'''
def decisao_desvio(camera):
    path = camera.Take_photo()
    objeto_imagem = classes.Classe_imagem(path)
    print("Antes da borda inferior")
    x, y = ponto_medio_borda_inferior(objeto_imagem)
    print("Antes da bordas_laterais_v2")
    lista_esquerda, lista_direita, caso = bordas_laterais_v2(objeto_imagem)
    print("Antes dos calculos de coef_angular e coef_linear")
    poly_left = [coef_angular(lista_esquerda), coef_linear(lista_esquerda)]
    poly_right = [coef_angular(lista_direita), coef_linear(lista_direita)]
    # caso = 1: linha central. caso = 2: borda direita. caso = 3: borda esquerda. caso = 0: nenhuma borda
    pixel_scale = 20.4
    d_min = 40
    x_robot = 0
    if x == 0 and y == 0:
        # Nao detectou obstaculo
        return ANDAR
    else:
        if caso == HA_DUAS_RETAS:
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
        if caso == SO_DIREITA:
            poly_inv = [1/poly_right[0], -poly_right[1]/poly_right[0]]
            x_linha = poly_inv[1] + poly_inv[0]*y
            if abs(x - x_linha) > d_min*pixel_scale:
                return GIRAR_DIREITA
            else:
                return GIRAR_ESQUERDA
        if caso == SO_ESQUERDA:
            poly_inv = [1/poly_left[0], -poly_left[1]/poly_left[0]]
            x_linha = poly_inv[1] + poly_inv[0]*y
            if abs(x - x_linha) > d_min*pixel_scale:
                return GIRAR_ESQUERDA
            else:
                return GIRAR_DIREITA
        if caso == NAO_HA_RETA: return ANDAR

casos_dic = ["NAO_HA_RETA", "HA_DUAS_RETAS", "SO_ESQUERDA", "SO_DIREITA"]

'''Recebe o sensor camera, uma tolerancia em relacao ao centro da imagem, e uma tolerancia em relacao ao quanto eh possivel
andar sem encontrar uma borda lateral para retornar uma direcao de giro ou entao andar em frente a partir das bordas.
Usada em todos os loops'''
def checar_alinhamento_pista_v1(camera, tolerancia_central, tolerancia_para_frente):
    path = camera.Take_photo()
    objeto_imagem = classes.Classe_imagem(path)
    reta_esquerda, reta_direita, caso = bordas_laterais_v2(objeto_imagem)
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
def checar_alinhamento_pista_v2(camera):
    path = camera.Take_photo()
    objeto_imagem = classes.Classe_imagem(path)
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