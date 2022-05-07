from time import sleep, time
import os
import numpy as np
import picamera
import constantes as c


class Camera():
    def __init__(self):
        # print("Entra no _init_ da Classe_camera")
        camera = picamera.PiCamera(resolution=(
            c.WIDTH, c.HEIGHT), framerate=c.FRAMERATE, contrast=c.CONTRAST)
        self.camera = camera
        sleep(c.WARMUP_TIME)

    def capture_opencv(self):
        image = np.empty((c.HEIGHT * c.WIDTH * 3,), dtype=np.uint8)
        self.camera.capture(image, 'bgr')
        image = image.reshape((c.HEIGHT, c.WIDTH, 3))
        return image

    def capture_sequence(self, frames):
#        camera.start_preview()
        # Give the camera some warm-up time
 #       time.sleep(2)
        start = time()
        self.camera.capture_sequence([
            '../data/images/sequence/image%02d.jpg' % i
            for i in range(frames)
            ], use_video_port=True)
        finish = time()
        print('Captured %d frames at %.2ffps' % (
        frames,
        frames / (finish - start)))

    def take_photo(self):
        try:
            self.path_atual = "./tests/fotos_main/imagem_main" + \
                str(self.indice_atual) + ".jpg"
            # print(" foto tirada em " + self.path_atual)
            self.camera.capture(self.path_atual)
            self.indice_atual = (self.indice_atual + 1) % 10
            # print("Saindo do Take_photo()")
            return self.path_atual
        except KeyboardInterrupt: self.camera.stop_preview()

    def parar_fotografar(self, estado):
        atual = estado.Obter_estado_atual()
        estado.Trocar_estado("PARAR")
        img = self.Take_photo()
        estado.Trocar_estado(atual)
        return img
