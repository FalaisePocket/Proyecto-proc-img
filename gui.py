import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
import numpy as np
import matplotlib.pyplot as plt 
import nibabel as nib

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



mainWindow=tk.Tk()




####Es una imagen
currentFileDir=0
currentFile=0

currentFileData = 0
currentFileHeader = 0
currentImage=0
currentImageSlice=0

##El valor del color
currentColor=0


coordinates=[0,0]
#####Listeners####################
def changeFile():
    global currentFileData
    global currentFileHeader
    global currentImage
    global currentImageSlice
    currentFileHeader= currentFile.header
    currentFileData = currentFile.get_fdata()
    currentImage = currentFileData[currentImageSlice]
    ###Dibujo

    Draw()

def Draw():
    figura = Figure()
    subplot = figura.add_subplot(111)
    subplot.imshow(currentImage, cmap='viridis', interpolation='nearest')

    lienzo = FigureCanvasTkAgg(figura, master=imageFrame)
    lienzo.draw()
    lienzo.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)






def plot_listener(event):
    # Obtener las coordenadas del evento
    x = event.xdata
    y = event.ydata
    if x is not None and y is not None:
        print(f"Coordenadas del clic: x={x}, y={y}")    

def openFile():
    global currentFileDir
    global currentFile
    print(currentFileDir)
    currentFileDir = filedialog.askopenfilename( filetypes=(("Archivos nifti", "*.nii"),("Archivos Nifti comprimidos","*.nii.gz")))
    try:
        currentFile = nib.load(currentFileDir)
        changeFile()

    except:
        0
    print("Nyah~")

def salir():
    mainWindow.destroy()
####################################################################################################################################################


###menu de control a lo photoshop#######################################
controlMenu=tk.Menu(mainWindow)
mainWindow.config(menu=controlMenu)


menu_archivo = tk.Menu(controlMenu,tearoff=0)
controlMenu.add_cascade(label="File", menu=menu_archivo)
menu_archivo.add_command(label="Open File...", command=openFile)
menu_archivo.add_separator()
menu_archivo.add_command(label="Exit", command=salir)
########################################################################







###layout general#######################################################
mainFrame=tk.Frame(mainWindow)
mainFrame.pack()

toolFrame=tk.Frame(mainFrame, width=100, height=100)
imageFrame=tk.Frame(mainFrame, width=500, height=500)
viewFrame=tk.Frame(mainFrame, width=100, height=100)

toolFrame.grid(row=0, column=0, rowspan=3)
imageFrame.grid(column=1, row=0, columnspan=2, rowspan=2)
viewFrame.grid(column=1,row=2, columnspan=2)
########################################################################


###Lateral de barra de herramientas#####################################
########################################################################

###Layout de imagen#####################################################

########################################################################

###Barra de slider de la imagen y rotacion##############################
##slider de imagenes
slider=ttk.Scale(viewFrame)
slider.pack()

########################################################################







mainWindow.mainloop()