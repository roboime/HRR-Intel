"""Modulo com funcoes auxiliares a visao.py"""

X_1 = 0
Y_1 = 1
X_2 = 2
Y_2 = 3
INF = 9999.9

def coef_linear(lista):
    """Retorna o coeficiente linear de uma reta definida pelos pontos (x1,y1) e (x2,y2)
    na forma da lista [x1, y1, x2, y2]
    """
    if len(lista) != 0:
        return float(float(lista[Y_1]) - float(lista[X_1])*coef_angular(lista))
    else:   return 0

def coef_angular(lista):
    """Retorna o coeficiente angular de uma reta definida pelos pontos (x1,y1) e (x2,y2)
    na forma da lista [x1, y1, x2, y2].
    Se a reta for vertical, retorna INF.
    """
    if len(lista) != 0:
        if lista[X_2] != lista[X_1]:
            return float(float(lista[Y_2]-lista[Y_1]) / float(lista[X_2]-lista[X_1]))
        else:
            return INF
    else:
        return INF

def intersection(line1, line2):
    """Retorna as coordenadas x e y do ponto de interseccao (x, y) entre duas retas lin1 e line2
    na forma de uma lista [x1, y1, x2, y2]."""
    ang_l = coef_angular(line1)
    ang_r = coef_angular(line2)
    lin_l = coef_linear(line1)
    lin_r = coef_linear(line2)

    x_coord = (lin_r - lin_l) / (ang_l - ang_r)
    y_coord = ang_r * x_coord + ang_r
    #IMG = cv2.circle(IMG, (int(x),int(y)), radius=10, color=(0, 255, 255), thickness=-1)
    return int(x_coord), int(y_coord)
