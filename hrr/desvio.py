"""Modulo responsavel pelo desvio de obstaculo do robo"""

class __Desvio():
    def verificar_desvio():
        pass
class DesvioObstaculo(__Desvio):
    """Classe que instancia Robo e implementa as funcoes de desvio de obstaculo"""
    def __init__(self, robo):
        self.robo = robo

    def __realinhagem(self):
        pass
    def __ultrapassagem(self):
        pass
    def __giro(self):
        pass
    def __decisao(self):
        pass
    def __proximidade(self):
        pass
    def verificar_desvio(self):
        """implementar"""

class DesvioDegrau(__Desvio):
    def __init__(self, robo):
        self.robo = robo
    def __descida(self):
        pass
    def __subida(self):
        pass
    def __proximidade(self):
        pass

    def verificar_desvio(self):
        pass

        
