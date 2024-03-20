
def isoData(slice,umbral):
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

