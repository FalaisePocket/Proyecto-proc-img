
import numpy as np

def kmeans(file, k=2, max_iters=10):
    file = np.asarray(file)  # Asegurar que sea un numpy array
    new_img = np.array([
        apply_threshold(slice, np.mean(k_means(slice, k, max_iters)))
        for slice in file
    ])
    return new_img

def k_means(pixels, k=2, max_iters=10):
    pixels = pixels.flatten()  # Asegurar que trabajamos con un array 1D
    centroids = np.random.choice(pixels, k, replace=False)

    for _ in range(max_iters):
        distances = np.abs(pixels[:, None] - centroids)  # Distancias a los centroides
        clusters = np.argmin(distances, axis=1)  # Índices de clusters

        # Recalcular centroides con seguridad (evitar clusters vacíos)
        new_centroids = np.array([
            pixels[clusters == j].mean() if np.any(clusters == j) else centroids[j]
            for j in range(k)
        ])

        if np.allclose(centroids, new_centroids):
            break
        centroids = new_centroids

    return centroids

def apply_threshold(image, threshold):
    return (image > threshold).astype(np.uint8) * 255  # Mantener valores de imagen binaria