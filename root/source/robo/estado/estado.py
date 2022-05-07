from porta_serial.porta_serial import PortaSerial
from time import sleep
import constantes as c

class Estado:
    def __init__(self):
        self.tempo_do_passo = {
            "ANDAR" : c.TEMPO_ANDAR,
            "GIRAR_ESQUERDA" : c.TEMPO_GIRAR_ESQUERDA,
            "GIRAR_DIREITA" : c.TEMPO_GIRAR_DIREITA,
            "PARAR" : c.TEMPO_PARAR
        }
        self.atual = "PARAR"
        self.myrio = PortaSerial()
        self.Trocar_estado("PARAR")

    def Obter_estado_atual(self):
        return self.atual
    
    def __str__(self):          #string associada ao objeto de "Classe_estado". Sera mostrada ao printar um objeto desse tipo
        
        need = {
            "ANDAR" : "NAO ha necessidade de correcao",   #Dicionario que associa o indice do estado a necessidade de correcao
            "GIRAR_ESQUERDA" : "Deve estar girando para esquerda",     
            "GIRAR_DIREITA" : "Deve estar girando para direita",
            "PARAR" : "Deve estar parado",
            "SUBIR" : "Deve estar subindo o degrau",
            "DESCER" : "Deve estar descendo o degrau"
                }
        atual = self.Obter_estado_atual()
        return f'Estado atual: {atual}.\nCorrecao: {need[atual]}.\n\n'
        
    def Trocar_estado(self, next_state):
        if next_state != self.atual:
            if next_state != "PARAR":
                self.atual = "PARAR"
                self.myrio.Escrever_estado("PARAR")
                sleep(self.lista_tempos["PARAR"])
            self.atual = next_state
            self.myrio.Escrever_estado(next_state)
            sleep(self.lista_tempos[next_state])
            print(self)
        else:
            print(f'Mantive o estado : {self.atual}')