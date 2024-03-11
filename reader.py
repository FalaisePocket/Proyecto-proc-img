import os
import numpy as np
import matplotlib.pyplot as plt 
##%matplotlib inline
import nibabel as nib # common way of importing nibabel

##carga la imagen
mri_file = 'brain_ct.nii'
img = nib.load(mri_file)
##Guarda las dimensiones de la imagen
dimensiones= img.shape

header = img.header
##Las imagenes de los archivos
img_data = img.get_fdata()



