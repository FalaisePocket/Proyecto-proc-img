import numpy as np
from scipy.sparse import lil_matrix, identity, diags
from scipy.sparse.linalg import spsolve
from scipy.ndimage import maximum_filter

def laplacian_segmentation(image: np.ndarray, seeds: np.ndarray, beta=90, eps=1e-6):
    if not ((seeds == 1).any() and (seeds == -1).any()):
        raise ValueError("Se necesitan al menos una semilla de fondo (1) y una de objeto (-1).")
    assert image.shape == seeds.shape, "Imagen y semillas deben tener la misma forma."
    
    height, width = image.shape
    n_pixels = height * width
    image_flat = image.flatten()
    
    # Cálculo de sigma global (normalización del peso)
    diffs = np.abs(image - maximum_filter(image, size=3, mode='nearest'))
    sigma = np.max(diffs)
    
    # Crear matrices dispersas
    W = lil_matrix((n_pixels, n_pixels))
    D = np.zeros(n_pixels)

    # Vecindario 8-conectado
    offsets = [(1, 0),(1, 1) ,(0, 1),(0, -1),(-1, 0),  (-1, -1), (1, -1),(-1, 1)]

    for i in range(height):
        for j in range(width):
            idx = i * width + j
            Ii = image[i, j]
            for dy, dx in offsets:
                ni, nj = i + dy, j + dx
                if 0 <= ni < height and 0 <= nj < width:
                    nidx = ni * width + nj
                    Ij = image[ni, nj]
                    diff = np.abs(Ii - Ij)
                    w = np.exp(-beta * (diff**2) / sigma)+eps
                    W[idx, nidx] = w
                    D[idx] += w

    # Matriz Laplaciana L = D - W
    D_sparse = lil_matrix((n_pixels, n_pixels))
    D_sparse.setdiag(D)
    L = D_sparse - W

    # L2 = L.T @ L
    L2 = L @ L

    # Construcción de sistema lineal (IS + L^2)x = b
    
    ##IS = identity(n_pixels, format='lil')

    #IS = IS.multiply(S[:, np.newaxis])  # 1 en posiciones con semilla, 0 en el resto
    S = (seeds != 0).flatten()
    IS = diags(S.astype(float))
    ##esto es lo mismo que b = seeds.flatten(), cambiar
    b = np.zeros(n_pixels)
    b[seeds.flatten() == 1] = 1
    b[seeds.flatten() == -1] = -1

    A = IS + L2
    print("A shape:", A.shape)
    print("A nnz:", A.nnz)
    x = spsolve(A.tocsr(), b)

    # Clasificación binaria
    mask = np.where(x >= 0, 1, 0).reshape((height, width))
    ##se compara con la imagen original
    result = mask * image 
    return result
