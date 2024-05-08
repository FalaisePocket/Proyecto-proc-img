import tkinter as tk
from tkinter import filedialog
import nibabel as nib
import numpy as np
from PIL import Image, ImageTk

def load_nii_and_display():
    filepath = filedialog.askopenfilename(filetypes=[("NIfTI files", "*.nii")])
    if filepath:
        nii_data = nib.load(filepath)
        img_data = nii_data.get_fdata()
        
        # Convertir los datos a uint8
        img_data = img_data.astype(np.uint8)
        
        img = Image.fromarray(img_data)
        img_tk = ImageTk.PhotoImage(img)

        # Actualizar la imagen mostrada en el lienzo
        canvas.image = img_tk
        canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)

# Crear la ventana principal
root = tk.Tk()
root.title("Visualizador de Imágenes NIfTI")

# Crear lienzo para mostrar la imagen
canvas = tk.Canvas(root, width=400, height=400)
canvas.pack()

# Botón para cargar archivo .nii
load_button = tk.Button(root, text="Cargar archivo .nii", command=load_nii_and_display)
load_button.pack()

# Ejecutar el bucle principal de la aplicación
root.mainloop()