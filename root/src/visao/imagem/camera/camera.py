import picamera

class Camera():
    def __init__(self):
        print("Entra no _init_ da Classe_camera")
        self.camera = picamera.PiCamera()
        self.intervalo_foto = 0.25
        self.indice_atual = 0
        self.path_pasta = os.path.dirname(os.path.abspath(__file__))
        self.path_atual = self.path_pasta + "1.jpg"

    def take_photo(self):
        self.camera.start_preview()
        self.camera.contrast = constraste_da_camera
        time.sleep(self.intervalo_foto)
        try:
            self.path_atual = "./tests/fotos_main/imagem_main" + str(self.indice_atual) + ".jpg"
            print(" foto tirada em " + self.path_atual)
            self.camera.capture(self.path_atual)
            self.camera.stop_preview()
            self.indice_atual = (self.indice_atual + 1) % 10
            print("Saindo do Take_photo()")
            return self.path_atual
        except KeyboardInterrupt: self.camera.stop_preview()


    def parar_fotografar(self, estado):
        atual = estado.Obter_estado_atual()
        estado.Trocar_estado(PARAR)
        img = self.Take_photo()
        estado.Trocar_estado(atual)
        return img