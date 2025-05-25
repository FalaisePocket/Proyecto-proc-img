import numpy as np

w=[]
v=[]
e=[]


def setgraphweight(img):
    sigma = max(np.linalg.norm(I[i] - I[j], ord=np.inf) for i, j in edges)
    
    weights = {}
    for i, j in img:
        diff_norm = np.linalg.norm(I[i] - I[j], ord=np.inf)
        weight = np.exp(-beta * (diff_norm**2) / sigma)
        weights[(i, j)] = weight

    return weights
    


def e(x):
    k1=0
    k2=0
    k3=0
    sumB=0
    sumF=0
    sumV=0
    F=[]
    B=[]
    V=[]
    N=[]
    d=[]
    for i in B:
        sumB+=x[i]-x[B]

    for i in F:
        sumF+=x[i]-x[F]
    
    for i in V:
        sumN=0
        for j in N[i]:
            sumN+=w[j][i]*x[j]

        sumV+=(d[i]*x[i])-sumN
    
    functionresult=(k1*sumB)+(k2*sumF)+(k3*sumV)


    return 0