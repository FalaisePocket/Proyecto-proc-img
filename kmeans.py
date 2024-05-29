import numpy as np

def kmeans(file,k=2):
    newImg=[]
    for slice in file:
        centroids = k_means(slice, k=2)
        threshold = np.mean(centroids)
        binary_image = apply_threshold(slice, threshold)
        newImg.append(binary_image)

        
    return np.array(newImg)



def k_means(pixels, k=2, max_iters=10):
    # Inicializar centroides al azar
    centroids = np.random.choice(pixels.flatten(), k)
    
    for _ in range(max_iters):
        # Asignar clusters
        distances = np.array([np.abs(pixels - centroid) for centroid in centroids])
        clusters = np.argmin(distances, axis=0)
        
        # Recalcular centroides
        new_centroids = np.array([pixels[clusters == j].mean() for j in range(k)])
        if np.all(centroids == new_centroids):
            break
        centroids = new_centroids
    
    return centroids

def apply_threshold(image, threshold):
    return (image > threshold) * 255



'''# Carga y procesamiento de la imagen
image_path = 'tu_imagen.jpg'
gray = load_image(image_path)

# Aplicar K-means
centroids = k_means(gray, k=2)
threshold = np.mean(centroids)

# Aplicar thresholding
binary_image = apply_threshold(gray, threshold)
'''