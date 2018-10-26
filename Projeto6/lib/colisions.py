from math import sqrt, isclose

def distance(a,b):
    """
    Distancia entre os pontos a e b
    """
    return sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

def is_between(a,c,b):
    """
    Verifica se o ponto c está entre os pontos a e b.
    """
    r = isclose(distance(a,c) + distance(c,b), distance(a,b))
    print(r)
    return r

def is_out(dot, sizex, sizey):
    """
    Verifica se o ponto ainda está nos limites da tela
    """
    if(dot[0] < 0 or dot[1] < 0):
        return True
    elif(dot[0] > sizex or dot [1] > sizey):
        return True
    else:
        return False
