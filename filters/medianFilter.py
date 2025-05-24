import numpy as np
def medianFiltffffffffffffer(img):
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



import numpy as np

def medianFilter(img):
    # Crear un array de salida con la misma forma
    resultado = np.zeros_like(img)
    # Dimensiones del volumen
    profundidad, filas, columnas = img.shape

    # Aplicar el filtro de mediana
    for z in range(profundidad):
        for i in range(filas):
            for j in range(columnas):
                # Obtener los valores vecinos en 3D
                vecinos = []
                for dz in range(-1, 2):
                    for dx in range(-1, 2):
                        for dy in range(-1, 2):
                            nz, ni, nj = z + dz, i + dx, j + dy
                            if 0 <= nz < profundidad and 0 <= ni < filas and 0 <= nj < columnas:
                                vecinos.append(img[nz, ni, nj])
                # Calcular la mediana de los valores vecinos
                vecinos.sort()
                mediana = vecinos[len(vecinos) // 2] if len(vecinos) % 2 != 0 else (vecinos[len(vecinos) // 2 - 1] + vecinos[len(vecinos) // 2]) // 2
                resultado[z, i, j] = mediana

    return resultado
