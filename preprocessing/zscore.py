import numpy as np

def zScore(img):
    mean = np.mean(img)
    std_dev = np.std(img)
    newImage= (img - mean) / std_dev
    return newImage


hola=np.array([])
print(type(hola))