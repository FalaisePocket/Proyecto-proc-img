


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
