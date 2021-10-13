from classes import Classe_camera, Classe_distancia
from time import sleep

dist = Classe_distancia()
camera = Classe_camera()

tempo = int(input("Entre com o tempo entre as fotos"))
numero_fotos = int(input("Entre com o numero de fotos"))
for i in range(numero_fotos):
    camera.Take_photo()
    print("Foto 1: dist = ", dist.Get_distance())
    print("tirei a foto, proxima foto em: ")
    for j in range(tempo):
        print(tempo-j) ##fazer a contagem regressiva  
        sleep(1)
