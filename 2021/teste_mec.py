from classes import Classe_porta_serial
from classes import Classe_estado
from constantes import *


myrio = Classe_porta_serial()
estado = Classe_estado(myrio, tempo_do_passo)

def main():
    print("Os codigos possiveis sao:\nANDAR: 0\nGIRAR_ESQUERDA: 1\nGIRAR_DIREITA: 2\nPARAR: 3\nSUBIR: 4\nDESCER: 5\n")

    while(True):
        k = str(input("Entre com um codigo(0-5): "))
        estado.Trocar_estado(k, myrio)


if __name__ == "__main__":
    try:
        main()
    except:
        print(" CTRL+C detectado. O loop foi interrompido.")
    estado.Trocar_estado(PARAR, myrio)