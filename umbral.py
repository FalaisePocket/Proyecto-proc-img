def umbralization(file,umbral):
    lista_matrices_umbralizadas = []
    for slice in file:
        matriz_umbralizada = aplicar_umbralizacion(slice, umbral)
        lista_matrices_umbralizadas.append(matriz_umbralizada)
    return lista_matrices_umbralizadas

def aplicar_umbralizacion(matriz, umbral):
    matriz_umbralizada=[[255 if pixel > umbral else 0 for pixel in fila] for fila in matriz]
    return matriz_umbralizada


