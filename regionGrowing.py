import numpy as np

def region_growing_3d(image, seed, threshold):
    mask = np.zeros(image.shape)

    # Agregar el punto de semilla a la región
    region_pixels = [seed]
    # Mientras haya puntos en la región
    while len(region_pixels) > 0:
        # Obtener el primer punto de la lista de region_pixels
        current_point = region_pixels[0]
        # Verificar los vecinos del punto actual
        for neighbor in [(current_point[0]+1, current_point[1], current_point[2]),
                         (current_point[0]-1, current_point[1], current_point[2]),
                         (current_point[0], current_point[1]+1, current_point[2]),
                         (current_point[0], current_point[1]-1, current_point[2]),
                         (current_point[0], current_point[1], current_point[2]+1),
                         (current_point[0], current_point[1], current_point[2]-1)]:
            # Verificar si el vecino está dentro de la imagen
            if (neighbor[0] < 0 or neighbor[0] >= image.shape[0] or
                neighbor[1] < 0 or neighbor[1] >= image.shape[1] or
                neighbor[2] < 0 or neighbor[2] >= image.shape[2]):
                continue
            # Verificar si el vecino no ha sido visitado y si su diferencia de intensidad con el punto de semilla es menor que el umbral
            if (mask[neighbor] == 0 and
                abs(int(image[neighbor]) - int(image[current_point])) < threshold):
                # Agregar el vecino a la región
                region_pixels.append(neighbor)
                # Marcar el vecino como visitado en la máscara
                mask[neighbor] = 1
        # Eliminar el punto actual de la lista de region_pixels
        region_pixels.pop(0)
    return mask


