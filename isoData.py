import numpy as np

def isoData111(slice,umbral):
    img=slice
    f=0
    t=0
    umbral_t=umbral
    tol=0.005
    while 1:
        f=img > umbral_t
        mL = img[f==1].mean()
        mH = img[f==0].mean()
        umbral_t1 = (mL+mH)/2
        if abs(umbral_t1-umbral_t)<tol:
            break
        umbral_t=umbral_t1
        t+=1
    return f



def isoData(image, initial_threshold, delta_t=0.005):
    t = 0
    tau = initial_threshold

    while True:
        # Aplicar umbralización
        g_t = image >= tau
        
        # Calcular las medias de los píxeles en el foreground y background
        if np.any(g_t):
            m_foreground = np.mean(image[g_t])
        else:
            m_foreground = 0
        
        if np.any(~g_t):
            m_background = np.mean(image[~g_t])
        else:
            m_background = 0
        
        # Actualizar el umbral
        tau_new = 0.5 * (m_foreground + m_background)
        
        # Verificar condición de parada
        if abs(tau_new - tau) < delta_t:
            break
        
        tau = tau_new
        t += 1

    return g_t


