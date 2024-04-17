import numpy as np
def meanFilter(img):
    '''#x,y
    coor=[
        [-1,-1],[0,-1],[+1,-1],
        [-1,0],        [1,0],
        [-1,+1],[0,+1],[1,1]]
    newData=[]
    for slice in img:
        newSlice=[]
        for y in range(len(slice)):
            for x in range(len(slice[y])):
                count=0
                for xy in coor:
                    count+= slice[y + xy[1] ][x + xy[0] ]'''
    newData=[]
    for slice in img:
        resultado = np.zeros_like(slice)
        filas, columnas = slice.shape
        for i in range(len(slice)):
            for j in range(len(slice[i])):
                # Calcular el promedio de los valores vecinos
                suma = 0
                contador = 0
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        if 0 <= i + dx < filas and 0 <= j + dy < columnas:
                            suma += slice[i + dx, j + dy]
                            contador += 1
                resultado[i, j] = suma // contador
        newData.append(resultado)

    return np.array(newData)