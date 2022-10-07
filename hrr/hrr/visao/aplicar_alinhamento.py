"Modulo usado para aplicar o algoritmo de decisao_alinhamento() da classe Visao() em imagens"
from os import listdir
from os.path import  join
import cv2
from .visao import Visao

PATH = "./data/images/input_imgs/"
VISAO = [Visao.from_path(join(PATH, f)) for f in listdir(join(PATH))]

FONT                   = cv2.FONT_HERSHEY_SIMPLEX
BOTTOM_LEFT_CORNER_OF_TEXT = (10,30)
FONT_SCALE              = 1
FONT_COLOR              = (255,255,255)
LINE_TYPE               = 2

def main():
    """Itera pelas imagens abertas, aplica o alinhamento e as salva na pasta de saida"""
    cnt=1
    for obj in VISAO:
        ret = obj.decisao_alinhamento()
        obj.desenhar_bordas()
        obj.desenhar_alinhamento()
        cv2.putText(obj.img,
                    ret,
                    BOTTOM_LEFT_CORNER_OF_TEXT,
                    FONT,
                    FONT_SCALE,
                    FONT_COLOR,
                    LINE_TYPE)
        cv2.imwrite("./data/images/teste_alinhamento/"+str(cnt)+".png", obj.img)
        cnt+=1
if __name__ == "__main__":
    main()
    