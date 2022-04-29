from porta_serial.porta_serial import PortaSerial

class Estado:
    def __init__(self, myrio, lista_tempos):
        self.lista_tempos = lista_tempos
        self.atual = PARAR
        self.serial_obj = myrio
        self.name = {    ANDAR : "ANDAR",
                    GIRAR_ESQUERDA : "GIRAR PARA A ESQUERDA",                      #Dicionario que associa o indice do estado ao nome
                    GIRAR_DIREITA : "GIRAR PARA A DIREITA",
                    PARAR : "PARAR",
                    SUBIR : "SUBIR",
                    DESCER : "DESCER"
                }
        self.Trocar_estado(PARAR)

    def Obter_estado_atual(self):
        return self.atual
    
    def __str__(self):          #string associada ao objeto de "Classe_estado". Sera mostrada ao printar um objeto desse tipo
        
        need = {
            ANDAR : "NAO ha necessidade de correcao",   #Dicionario que associa o indice do estado a necessidade de correcao
            GIRAR_ESQUERDA : "Deve estar girando para esquerda",     
            GIRAR_DIREITA : "Deve estar girando para direita",
            PARAR : "Deve estar parado",
            SUBIR : "Deve estar subindo o degrau",
            DESCER : "Deve estar descendo o degrau"
                }
        atual = self.Obter_estado_atual()
        return "Estado atual: " + self.name[atual] + ".\nCorrecao: " + need[atual] + ".\n\n"
        
    def Trocar_estado(self, next_state):
        if next_state != self.atual:
            if next_state != PARAR:
                self.atual = PARAR
                self.serial_obj.Escrever_estado(PARAR)
                time.sleep(self.lista_tempos[(PARAR)])
            self.atual = next_state
            self.serial_obj.Escrever_estado(next_state)
            time.sleep(self.lista_tempos[(next_state)])
            print(self.__str__())
        else:
            print("Mantive o estado :" , self.name[self.atual])