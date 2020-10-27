#Código responsável por fazer o robô girar
"""
Created on Oct 2020
    Funçoes
    GetDistance

@author: Clarisse Rufino
"""
def direcao_desvio(yaw_0, Dmin):
    distancia_0 = 0
    distancia_1 = Distancia.getDistance()
    while True:
        distancia_0 = Distancia.getDistance()
        if distancia_0 > Dmin:
           Yaw = Direcao.getYaw() - yaw_0
            return 3, Yaw, distancia_1
            else:
                distancia_1 = distancia_0




