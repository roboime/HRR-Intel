import funcoes


ANDAR = "0"                 
GIRAR_ESQUERDA = "1"        
GIRAR_DIREITA = "2"         
PARAR = "3"
SUBIR = "4"
DESCER = "5"

tolerancia_central = 15
tolerancia_para_frente = 60

class Classe_camera():
    def __init__(self):
        self.path_atual = "./tests/fotos_main/imagem_main3.jpg"

    def Take_photo(self):
        return self.path_atual

class Classe_estado:
    def __init__(self):
        self.atual = PARAR
        self.Trocar_estado(PARAR)

    def Obter_estado_atual(self):
        return self.atual
    
    def __str__(self):          #string associada ao objeto de "Classe_estado". Sera mostrada ao printar um objeto desse tipo
        name = {    ANDAR : "ANDAR",
                    GIRAR_ESQUERDA : "GIRAR PARA A ESQUERDA",                      #Dicionario que associa o indice do estado ao nome
                    GIRAR_DIREITA : "GIRAR PARA A DIREITA",
                    PARAR : "PARAR",
                    SUBIR : "SUBIR",
                    DESCER : "DESCER"
                }
        need = {
            ANDAR : "NAO ha necessidade de correcao",   #Dicionario que associa o indice do estado a necessidade de correcao
            GIRAR_ESQUERDA : "Deve estar girando para esquerda",     
            GIRAR_DIREITA : "Deve estar girando para direita",
            PARAR : "Deve estar parado",
            SUBIR : "Deve estar subindo o degrau",
            DESCER : "Deve estar descendo o degrau"
                }
        atual = self.Obter_estado_atual()
        return "Estado atual: " + name[atual] + ".\nindice: " + str(atual) + ".\nCorrecao: " + need[atual] + ".\n\n"
        
    def Trocar_estado(self, state):
        self.atual = state
        print(self.__str__())



def main():
    camera = Classe_camera()
    estado = Classe_estado()
    estado.Trocar_estado(funcoes.checar_alinhamento_pista_v1(camera, tolerancia_central, tolerancia_para_frente))
    #estado.Trocar_estado(funcoes.checar_alinhamento_pista_v2(camera))

if __name__ == "__main__": main()