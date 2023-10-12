from robo import Robo
from serial_com import SerialMyrio

class CriarRobo:
    def __init__(self, robo: Robo):
        """Inicializa com instancias das classes Estado, Visao, Imu e Alinhamento"""
        self.robo = robo

    def main(self):
        try:
            self.robo.corrida()
        except KeyboardInterrupt:
            print(" CTRL+C detectado. O loop foi interrompido.")
            y = SerialMyrio()
            while(1):
                y.parar()
        

x = CriarRobo()
x.main()
        

