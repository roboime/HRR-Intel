"""Modulo responsavel pelo desvio de obstaculo do robo"""

# class Desvio(ABC):
#     def verificar_desvio():
#         pass
# class DesvioObstaculo(Desvio):
#     """Classe que instancia Robo e implementa as funcoes de desvio de obstaculo"""
#     def __init__(self, robo):
#         self.robo = robo

#     def __realinhagem(self):
#         pass
#     def __ultrapassagem(self):
#         pass
#     def __giro(self):
#         pass
#     def __decisao(self):
#         pass
#     def __proximidade(self):
#         pass
#     def verificar_desvio(self):
#         """implementar"""

# class DesvioDegrau(Desvio):
#     def __init__(self, robo):
#         self.robo = robo
#     def __descida(self):
#         pass
#     def __subida(self):
#         pass
#     def __proximidade(self):
#         pass

#     def verificar_desvio(self):
#         pass

        
class DesvioDegrau:
    def __init__(self, robo) -> None:
        self.__robo = robo

    @property
    def robo(self):
        return self.__robo


class DesvioObstaculo:
    def __init__(self, robo) -> None:
        self.__robo = robo

    @property
    def robo(self):
        return self.__robo


class Desvio(DesvioObstaculo, DesvioDegrau):
    def __init__(self, robo) -> None:
        DesvioObstaculo.__init__(self, robo)
        DesvioDegrau.__init__(self, robo)

if __name__ == '__main__':
    from robo import Robo
    robo = Robo()
    desvio = Desvio(robo)