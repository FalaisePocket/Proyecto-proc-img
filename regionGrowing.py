import numpy as np
from collections import deque

def region_growing_3d(image, seed, threshold):
    """
    Segmentación de crecimiento de región en una imagen 3D.

    :param image: Matriz 3D (numpy array) de la imagen.
    :param seed: Punto de inicio (x, y, z) como una tupla.
    :param threshold: Umbral para la diferencia de intensidad.
    :return: Máscara 3D con la región segmentada (1 dentro de la región, 0 fuera).
    """

    # Inicializar máscara de la misma forma que la imagen
    mask = np.zeros_like(image, dtype=np.uint8)

    # Verificar que el punto de inicio está dentro de los límites
    if not (0 <= seed[0] < image.shape[0] and 
            0 <= seed[1] < image.shape[1] and 
            0 <= seed[2] < image.shape[2]):
        raise ValueError("El punto de inicio está fuera de los límites de la imagen")

    # Inicializar la cola con el punto de inicio
    queue = deque([seed])
    mask[seed] = 1  # Marcar el punto de inicio en la máscara
    seed_value = image[seed]  # Intensidad del punto de inicio

    # Desplazamientos en las 6 direcciones posibles (adyacencia 6-conexa en 3D)
    neighbors = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]

    while queue:
        x, y, z = queue.popleft()  # Obtener y eliminar el primer elemento

        for dx, dy, dz in neighbors:
            nx, ny, nz = x + dx, y + dy, z + dz  # Calcular vecino

            # Verificar que el vecino esté dentro de los límites
            if 0 <= nx < image.shape[0] and 0 <= ny < image.shape[1] and 0 <= nz < image.shape[2]:

                # Verificar si el píxel no ha sido visitado y cumple con el umbral
                if mask[nx, ny, nz] == 0 and abs(int(image[nx, ny, nz]) - int(seed_value)) < threshold:
                    mask[nx, ny, nz] = 1  # Marcar píxel como parte de la región
                    queue.append((nx, ny, nz))  # Agregar vecino a la cola

    return mask