#!/usr/bin/env python
# coding: utf-8


"""
Created on Sept 2020
    Funçoes
    GetDistance

@author: Domingos
"""



######################## Libraries #############################

import VL53L0X              
import time                                




"""Função principal"""
if __name__ == '__main__':
    """Criar uma instancia de VL53L0X"""
    tof = VL53L0X.VL53L0X(address=0x29)

    #Pedido de distancia
    tof.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)

    try:
        while True:
            dist = tof.get_distance()/float(10)   #distancia de VL53L0X para obter a [cm]
            print ("%0.1f cm " % dist)     #distancia [cm] para exibir o 
            time.sleep(1)               #1[s]sleep
    except KeyboardInterrupt  :         #Termina o loop com CTRL+C
        print("\nCtl+C")
    except Exception as e:
        print(str(e))                   #Exibir o conteudo do procesamento de exceções do console
    finally:
        tof.stop_ranging()              #VL53L0X finalizar processamento 
        print("\nexit program")         #Exibir programa terminado

