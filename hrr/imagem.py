import cv2 as cv
from functools import lru_cache


class Imagem:
    '''
    Classe que envolve operações a nível lógico com as imagens obtidas pela câmera.
    '''
    def __init__(self, path: str) -> None: pass

    def resize(self, width: int, height: int) -> None: pass

    def rotate(self, angle: int) -> None: pass

    def mask(self, ranges_file_path): pass

    def ponto_medio_borda_inferior(objeto_imagem): pass

    def bordas_laterais(self): pass

    def checar_proximidade(valor_comparar, imagem_path): pass

    def checar_alinhamento_pista_v2(objeto_imagem): pass