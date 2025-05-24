import numpy as np
def meanFilter(img):

    newData=[]
    for slice in img:##mover abajo
        resultado = np.zeros_like(slice)
        filas, columnas = slice.shape
        for i in range(len(slice)):
            for j in range(len(slice[i])):
                # Calcular el promedio de los valores vecinos
                suma = 0
                contador = 0
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        ##for dz
                        if 0 <= i + dx < filas and 0 <= j + dy < columnas:
                            suma += slice[i + dx, j + dy]
                            contador += 1
                resultado[i, j] = suma // contador
        newData.append(resultado)

    return np.array(newData)


import numpy as np

def meanFilter3D(img):
    # Crear un array de salida con la misma forma
    resultado = np.zeros_like(img)
    # Dimensiones del volumen
    profundidad, filas, columnas = img.shape

    for z in range(profundidad):
        for i in range(filas):
            for j in range(columnas):
                suma = 0
                contador = 0
                # Recorrer vecinos en 3D
                for dz in range(-1, 2):
                    for dx in range(-1, 2):
                        for dy in range(-1, 2):
                            nz, ni, nj = z + dz, i + dx, j + dy
                            if 0 <= nz < profundidad and 0 <= ni < filas and 0 <= nj < columnas:
                                suma += img[nz, ni, nj]
                                contador += 1
                # Asignar el valor promedio
                resultado[z, i, j] = suma // contador if contador != 0 else img[z, i, j]

    return resultado
