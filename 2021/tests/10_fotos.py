from time import sleep
import picamera


camera = picamera.PiCamera()
camera.resolution = (1024, 768)
camera.start_preview()

sleep(2)
#tempo = int(input("Entre com o tempo entre as fotos"))
#numero_fotos = int(input("Entre com o numero de fotos"))
tempo = 5
numero_fotos = 10
for i in range(numero_fotos):
    diretorio_com_nome = "/home/pi/HRR-Intel/2021/tests/imagem_teste_contraste_" + str(i) + ".jpg"
    camera.contrast = 90
    camera.capture(diretorio_com_nome)
    print("tirei a foto, proxima foto em: ")
    for j in range(tempo):
        print(tempo-j) ##fazer a contagem regressiva  
        sleep(1)

camera.stop_preview()
