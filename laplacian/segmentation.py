import numpy as np

w=[]
v=[]
e=[]


def setgraphweight(I, beta):
    sigma = max(np.linalg.norm(I[i] - I[j], ord=np.inf) for i, j in edges)
    
    weights = {}
    for i, j in I:
        diff_norm = np.linalg.norm(I[i] - I[j], ord=np.inf)
        weight = np.exp(-beta * (diff_norm**2) / sigma)
        weights[(i, j)] = weight

    return weights
    


def e(x, B, F, img,grafo):
    k1=1
    k2=1
    k3=1
    sumB=0
    sumF=0
    sumV=0
    
    d=[]
    for i in B:
        sumB+=x[i]-x[B]

    for i in F:
        sumF+=x[i]-x[F]
    
    for i in grafo:
        sumN=0
        for j in grafo[i]:
            sumN+=w[(i,j)]*x[j]

        sumV+=(d[i]*x[i])-sumN
    
    functionresult=(k1*sumB)+(k2*sumF)+(k3*sumV)


    return 0

def getAristas(img):
    vecinos = []
    filas, cols = img.shape
    for i in range(filas):
        for j in range(cols):
            for di in [-1, 0, 1]:
                for dj in [-1, 0, 1]:
                    if di == 0 and dj == 0:
                        continue 
                    ni, nj = i + di, j + dj
                    if 0 <= ni < filas and 0 <= nj < cols:
                        vecinos.append(((i, j), (ni, nj)))
    
    return vecinos



def crearGrafo(img,beta):
    alto,ancho=img.shape()
    nuevo_alto = 2 * alto - 1
    nuevo_ancho = 2 * ancho - 1
    flatImg=img.flatten()
    aristas=getAristas(img)
    sigma = max(np.linalg.norm(img[i] - img[j], ord=np.inf) for i, j in aristas)
    
    weights = {}
    for i, j in aristas:
        diff_norm = np.linalg.norm(img[i] - img[j], ord=np.inf)
        weight = np.exp(-beta * (diff_norm**2) / sigma)
        weights[(i, j)] = weight


   
    return 3

def laplacian_segmentation(img, seeds):
    ##se construye un grafo
    grafo=crearGrafo()




    return 0