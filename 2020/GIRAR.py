#Código responsável pela condição do robô girar ou não
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
        distancia_1 = distancia_0
        distancia_0 = Distancia.getDistance()
        if distancia_0 > Dmin:
            distancia_1 = distancia_0
            return 3
        time.sleep(0.4)




