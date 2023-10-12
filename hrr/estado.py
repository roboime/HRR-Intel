"""Modulo responsavel pela a maquina de estados do robo."""
from time import sleep
import constantes as c
from serial_com import SerialMyrio

class Estado:
    """Classe responsavel pela a maquina de estados do robo."""
    def __init__(self):
        """
        Inicia variaveis de tempo de intervalo para cada estado.
        Instancia objeto da classe porta_Serial correspondente, que envia os estados do robo para a
        placa por meio de comunicacao serial.
        """
        self.tempo_do_passo = {
            c.ANDAR : c.TEMPO_ANDAR,
            c.GIRAR_ESQUERDA : c.TEMPO_GIRAR_ESQUERDA,
            c.GIRAR_DIREITA : c.TEMPO_GIRAR_DIREITA,
            c.PARAR : c.TEMPO_PARAR,
            c.SUBIR : c.TEMPO_SUBIR,
            c.DESCER : c.TEMPO_DESCER
        }
        self.string_enum = {
            c.ANDAR : c.ANDAR,
            c.GIRAR_ESQUERDA : c.GIRAR_ESQUERDA,
            c.GIRAR_DIREITA : c.GIRAR_DIREITA,
            c.PARAR : c.PARAR,
            c.SUBIR  :  c.SUBIR,
            c.DESCER : c.DESCER
        }
        self.enum_string = {
            c.ANDAR: c.ANDAR  ,
            c.GIRAR_ESQUERDA: c.GIRAR_ESQUERDA ,
            c.GIRAR_DIREITA: c.GIRAR_DIREITA ,
            c.PARAR: c.PARAR,
            c.SUBIR: c.SUBIR,
            c.DESCER: c.DESCER 
        }
        self.atual = c.PARAR
        x = SerialMyrio()
        self.porta_serial = x.obter_porta()
        print(self.porta_serial)
        self.trocar_estado(c.PARAR)

    def obter_estado_atual(self):
        """Retorna o estado atual do robo."""
        return self.atual

    def __str__(self):
        """String associada ao objeto de "Estado". Sera mostrada ao printar um objeto desse tipo"""
        return "Estado atual: "+ self.atual + "\n"

    def trocar_estado(self, next_state):
        """Troca o estado atual do robo e o envia para a porta serial."""
        if next_state != self.atual:
            if next_state != c.PARAR:
                self.atual = c.PARAR
                SerialMyrio.escrever_estado(c.PARAR)
            self.atual = next_state
            SerialMyrio.escrever_estado(self.enum_string[next_state])
            print(self)
        else:
            print("Mantive o estado : " + self.atual + "\n")