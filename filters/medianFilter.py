import numpy as np
def medianFilter(img):
    newData=[]
    for slice in img:
        resultado = np.zeros_like(slice)
        # Dimensiones de la matriz
        filas, columnas = slice.shape

        # Aplicar el filtro de mediana
        for i in range(filas):
            for j in range(columnas):
                # Obtener los valores vecinos
                vecinos = []
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        if 0 <= i + dx < filas and 0 <= j + dy < columnas:
                            vecinos.append(slice[i + dx, j + dy])
                # Calcular la mediana de los valores vecinos
                vecinos.sort()
                mediana = vecinos[len(vecinos) // 2] if len(vecinos) % 2 != 0 else (vecinos[len(vecinos) // 2 - 1] + vecinos[len(vecinos) // 2]) // 2
                resultado[i, j] = mediana
        newData.append(resultado)
    return np.array(newData)