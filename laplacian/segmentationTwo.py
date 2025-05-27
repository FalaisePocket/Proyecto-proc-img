'''


import numpy as np
from scipy.sparse import lil_matrix, diags
from scipy.sparse.linalg import spsolve

def laplacian_segmentation(image: np.ndarray, seeds: np.ndarray, beta=90, epsilon=1e-6):
    """
    Segmentación por coordenadas laplacianas.
    
    Parámetros:
        image: np.ndarray [H x W x 3] o [H x W] - imagen RGB o grayscale
        seeds: np.ndarray [H x W] - mapa de semillas (1: fondo, -1: objeto, 0: desconocido)
        beta: float - parámetro para el cálculo de pesos
        epsilon: float - valor para evitar pesos nulos
        
    Devuelve:
        segmentacion binaria: np.ndarray [H x W] - 1 para fondo, 0 para objeto
    """
    H, W = seeds.shape
    N = H * W
    image_flat = image.reshape((-1, 3)) if image.ndim == 3 else image.reshape((-1, 1))

    # Paso 1: Calcular pesos del grafo (8 vecinos)
    def get_neighbors(i, j):
        for di in [-1, 0, 1]:
            for dj in [-1, 0, 1]:
                if di == 0 and dj == 0:
                    continue
                ni, nj = i + di, j + dj
                if 0 <= ni < H and 0 <= nj < W:
                    yield ni, nj

    W_mat = lil_matrix((N, N))
    max_diff = 0

    for i in range(H):
        for j in range(W):
            idx = i * W + j
            for ni, nj in get_neighbors(i, j):
                n_idx = ni * W + nj
                diff = np.abs(image[i, j] - image[ni, nj]) if image.ndim == 2 else np.max(np.abs(image[i, j] - image[ni, nj]))
                max_diff = max(max_diff, diff)

    sigma = max_diff if max_diff != 0 else 1

    for i in range(H):
        for j in range(W):
            idx = i * W + j
            for ni, nj in get_neighbors(i, j):
                n_idx = ni * W + nj
                diff = np.abs(image[i, j] - image[ni, nj]) if image.ndim == 2 else np.max(np.abs(image[i, j] - image[ni, nj]))
                weight = np.exp(-beta * (diff ** 2) / sigma) + epsilon
                W_mat[idx, n_idx] = weight

    # Paso 2: Construir matrices del sistema
    W_mat = W_mat.tocsr()
    d = np.array(W_mat.sum(axis=1)).flatten()
    D_mat = diags(d)
    L = D_mat - W_mat
    L2 = L.dot(L)

    # Paso 3: Construir sistema (IS + L^2)x = b
    seeds_flat = seeds.flatten()
    IS_diag = (seeds_flat != 0).astype(float)
    IS = diags(IS_diag)
    b = np.zeros(N)
    b[seeds_flat == 1] = 1  # fondo
    b[seeds_flat == -1] = -1  # objeto

    A = IS + L2
    x = spsolve(A, b)

    # Paso 4: Asignar etiquetas
    x = x.reshape((H, W))
    threshold = 0  # Como fondo=1, objeto=-1, umbral en 0
    segmented = np.where(x >= threshold, 1, 0)

    return segmented.astype(np.uint8)



import numpy as np
from scipy.sparse import lil_matrix, diags
from scipy.sparse.linalg import spsolve

def laplacian_segmentation(image: np.ndarray, seeds: np.ndarray, beta=90, epsilon=1e-6):
    """
    Segmentación por coordenadas laplacianas.

    Parámetros:
        image: np.ndarray [H x W x 3] o [H x W] - imagen RGB o escala de grises
        seeds: np.ndarray [H x W x 1] - semillas (-1: objeto, 0: sin etiqueta, 1: fondo)
        beta: float - parámetro de sensibilidad de peso
        epsilon: float - evita pesos nulos

    Retorna:
        np.ndarray [H x W] - segmentación binaria (1: fondo, 0: objeto)
    """
    # Si seeds es 3D con profundidad 1, aplanarlo a 2D
    if seeds.ndim == 3 and seeds.shape[2] == 1:
        seeds = seeds[:, :, 0]
    elif seeds.ndim != 2:
        raise ValueError("Las semillas deben tener forma (H, W, 1) o (H, W)")

    H, W = seeds.shape
    N = H * W
    image_flat = image.reshape((-1, 3)) if image.ndim == 3 else image.reshape((-1, 1))

    # Calcular pesos del grafo
    def get_neighbors(i, j):
        for di in [-1, 0, 1]:
            for dj in [-1, 0, 1]:
                if di == 0 and dj == 0:
                    continue
                ni, nj = i + di, j + dj
                if 0 <= ni < H and 0 <= nj < W:
                    yield ni, nj

    W_mat = lil_matrix((N, N))
    max_diff = 0

    for i in range(H):
        for j in range(W):
            for ni, nj in get_neighbors(i, j):
                diff = np.abs(image[i, j] - image[ni, nj]) if image.ndim == 2 else np.max(np.abs(image[i, j] - image[ni, nj]))
                max_diff = max(max_diff, diff)

    sigma = max_diff if max_diff != 0 else 1

    for i in range(H):
        for j in range(W):
            idx = i * W + j
            for ni, nj in get_neighbors(i, j):
                n_idx = ni * W + nj
                diff = np.abs(image[i, j] - image[ni, nj]) if image.ndim == 2 else np.max(np.abs(image[i, j] - image[ni, nj]))
                weight = np.exp(-beta * (diff ** 2) / sigma) + epsilon
                W_mat[idx, n_idx] = weight

    # Construir matrices
    W_mat = W_mat.tocsr()
    d = np.array(W_mat.sum(axis=1)).flatten()
    D_mat = diags(d)
    L = D_mat - W_mat
    L2 = L.dot(L)

    seeds_flat = seeds.flatten()
    IS_diag = (seeds_flat != 0).astype(float)
    IS = diags(IS_diag)
    b = np.zeros(N)
    b[seeds_flat == 1] = 1   # fondo
    b[seeds_flat == -1] = -1 # objeto

    A = IS + L2
    x = spsolve(A, b)

    # Clasificación final
    x = x.reshape((H, W))
    segmented = np.where(x >= 0, 1, 0).astype(np.uint8)

    return segmented






import numpy as np
from scipy.sparse import lil_matrix, diags
from scipy.sparse.linalg import spsolve

def laplacian_segmentation(image: np.ndarray, seeds: np.ndarray) -> np.ndarray:
    H, W, C = image.shape
    N = H * W

    # Preprocesamiento
    img = image.reshape(-1, C).astype(np.float32)
    seeds_flat = seeds.reshape(-1)
    
    # Crear matriz de adyacencia (8 vecinos)
    W_mat = lil_matrix((N, N))
    max_diff = 0.0
    beta = 90.0
    eps = 1e-6

    # Precalcular índice 2D → 1D
    def idx(y, x): return y * W + x

    # Calcular pesos
    for y in range(H):
        for x in range(W):
            i = idx(y, x)
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    if dy == 0 and dx == 0:
                        continue
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < H and 0 <= nx < W:
                        j = idx(ny, nx)
                        diff = np.max(np.abs(img[i] - img[j]))
                        max_diff = max(max_diff, diff)

    sigma = max_diff + eps

    # Llenar W_mat con los pesos
    for y in range(H):
        for x in range(W):
            i = idx(y, x)
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    if dy == 0 and dx == 0:
                        continue
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < H and 0 <= nx < W:
                        j = idx(ny, nx)
                        diff = np.max(np.abs(img[i] - img[j]))
                        w_ij = np.exp(-beta * (diff ** 2) / sigma)
                        W_mat[i, j] = w_ij

    W_mat = W_mat.tocsr()
    d = np.array(W_mat.sum(axis=1)).flatten()
    D = diags(d)
    L = D - W_mat

    # Construir sistema (IS + L^2)x = b
    L2 = L @ L
    IS = diags((seeds_flat != 0).astype(np.float32))
    A = IS + L2

    b = np.zeros(N, dtype=np.float32)
    b[seeds_flat == 1] = 1
    b[seeds_flat == -1] = -1

    # Resolver sistema lineal
    x = spsolve(A, b)

    # Clasificar según umbral (xB + xF)/2 = 0
    output = np.where(x >= 0, 1, -1).reshape(H, W)

    return output




import numpy as np
import scipy.sparse
import scipy.sparse.linalg

def laplacian_segmentation(image, seeds, beta=90):
    
    """
    Segmenta una imagen 3D utilizando el algoritmo de Laplacian Coordinates.
    
    Parámetros:
    - image: np.ndarray (3D), matriz de intensidades.
    - seeds: np.ndarray (3D), misma forma que `image`, valores {-1, 0, 1}.
    - beta: float, controla la sensibilidad a diferencias de intensidad.

    Retorna:
    - segmentation: np.ndarray (3D), valores {-1, 1}.
    """
    shape = image.shape
    N = np.prod(shape)
    image_flat = image.flatten()
    seeds_flat = seeds.flatten()

    indices = np.arange(N).reshape(shape)

    def neighbors(x, y, z):
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                for dz in [-1, 0, 1]:
                    if dx == dy == dz == 0:
                        continue
                    nx, ny, nz = x + dx, y + dy, z + dz
                    if 0 <= nx < shape[0] and 0 <= ny < shape[1] and 0 <= nz < shape[2]:
                        yield (nx, ny, nz)

    rows, cols, weights = [], [], []

    max_diff = 0.0
    for x in range(shape[0]):
        for y in range(shape[1]):
            for z in range(shape[2]):
                i = indices[x, y, z]
                for nx, ny, nz in neighbors(x, y, z):
                    j = indices[nx, ny, nz]
                    diff = abs(image[x, y, z] - image[nx, ny, nz])
                    max_diff = max(max_diff, diff)

    sigma = max_diff if max_diff > 0 else 1.0

    for x in range(shape[0]):
        for y in range(shape[1]):
            for z in range(shape[2]):
                i = indices[x, y, z]
                for nx, ny, nz in neighbors(x, y, z):
                    j = indices[nx, ny, nz]
                    diff = abs(image[x, y, z] - image[nx, ny, nz])
                    w = np.exp(-beta * (diff**2) / sigma)
                    rows.extend([i, j])
                    cols.extend([j, i])
                    weights.extend([w, w])  # simétrico

    W = scipy.sparse.coo_matrix((weights, (rows, cols)), shape=(N, N)).tocsr()
    D = scipy.sparse.diags(W.sum(axis=1).A1)
    L = D - W
    L2 = L @ L

    # Asegurar aplanado después de validación
    mask_foreground = (seeds == -1).flatten()
    mask_background = (seeds == 1).flatten()
    mask_seeds = mask_foreground | mask_background
    b = np.zeros(N)
    b[mask_background] = 1
    b[mask_foreground] = -1
    
    IS = scipy.sparse.diags(mask_seeds.astype(float))
    assert IS.shape == L2.shape, f"Shapes no coinciden: IS {IS.shape}, L2 {L2.shape}"
    A = IS + L2

    x = scipy.sparse.linalg.spsolve(A, b)
    x = x.reshape(shape)

    segmentation = np.where(x >= 0, 1, -1)
    return segmentation
    

'''


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
    sigma = np.max(diffs) + eps
    
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
                    w = np.exp(-beta * (diff**2) / sigma)
                    W[idx, nidx] = w
                    D[idx] += w

    # Matriz Laplaciana L = D - W
    D_sparse = lil_matrix((n_pixels, n_pixels))
    D_sparse.setdiag(D)
    L = D_sparse - W

    # L2 = L.T @ L
    L2 = L.T @ L

    # Construcción de sistema lineal (IS + L^2)x = b
    S = (seeds != 0).flatten()
    ##IS = identity(n_pixels, format='lil')

    #IS = IS.multiply(S[:, np.newaxis])  # 1 en posiciones con semilla, 0 en el resto
    IS = diags(S.astype(float))

    b = np.zeros(n_pixels)
    b[seeds.flatten() == 1] = 1
    b[seeds.flatten() == -1] = -1

    A = IS + L2
    print("A shape:", A.shape)
    print("A nnz:", A.nnz)
    x = spsolve(A.tocsr(), b)

    # Clasificación binaria
    result = np.where(x >= 0, 1, -1).reshape((height, width))
    return result
