X1 = 0
Y1 = 1
X2 = 2
Y2 = 3

def coef_linear(lista):
    if len(lista) != 0:
        return float(float(lista[Y1]) - float(lista[X1])*coef_angular(lista))
    else:   return 0

def coef_angular(lista):
    if len(lista) != 0:
        if lista[X2] != lista[X1]: return float(float(lista[Y2]-lista[Y1]) / float(lista[X2]-lista[X1]))
        else: return 999.9
    else: return 999.9

def intersection(r1, r2):
    ml = coef_angular(r1)
    mr = coef_angular(r2)
    nl = coef_linear(r1)
    nr = coef_linear(r2)

    x = (nr-nl)/(ml-mr)
    y = mr*x+nr
    #IMG = cv2.circle(IMG, (int(x),int(y)), radius=10, color=(0, 255, 255), thickness=-1)
    return int(x), int(y)  