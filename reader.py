import os
import numpy as np
import matplotlib.pyplot as plt 
import nibabel as nib

##carga la imagen
mri_file = ' '
img = nib.load(mri_file)
##Guarda las dimensiones de la imagen
dimensiones= img.shape

header = img.header
##Las imagenes de los archivos
img_data = img.get_fdata()



