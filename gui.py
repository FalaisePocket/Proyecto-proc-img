import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import nibabel as nib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from umbral import umbralization
from isoData import isoData
from regionGrowing import region_growing_3d
from filters.meanFilter import meanFilter
from filters.medianFilter import medianFilter
from PIL import Image,ImageTk
from kmeans import kmeans


mainWindow=tk.Tk()



####Es una imagen
currentFileDir=0
currentFile=0

currentFileData = 0
currentFileHeader = 0

currentImage=0
currentImageSlice=0

currentPosition=0


images=[]

##El valor del color
currentColor=0

y_click=0
x_click=0

overlay = None






#####Listeners####################
def changeFile():
    global currentFileData
    global currentFileHeader
    global currentImage
    global currentImageSlice
    global overlay
    currentFileHeader= currentFile.header
    currentFileData = currentFile.get_fdata()
    print(currentFileHeader)
    overlay = np.zeros_like(currentFileData, dtype=np.uint8)
    transformDataToImage()
    currentImage = images[currentImageSlice]

    ###Dibujo
    slider.config(from_=0, to=currentFileData.shape[2]-1,command=changeImage)
    
    
    Draw()


def Draw():
    global lienzo
    global images
    global currentImageSlice
    global imageFrame
    global lienzo, imagen_tk

    
    img = images[currentImageSlice].copy()
    
    # Agregar overlay de píxeles rojos
    applyOverlay(img)
    
    imagen_tk = ImageTk.PhotoImage(img)
    
    lienzo.configure(image=imagen_tk)
    lienzo.image = imagen_tk
    



def transformDataToImage():
    global images
    images = []
    
    for slice_idx in range(currentFileData.shape[2]):
        img_array = np.uint8((currentFileData[:, :, slice_idx] / np.max(currentFileData)) * 255)  # Normalizar a 0-255
        img = Image.fromarray(img_array, mode='L').convert("RGB")  # Convertir a RGB
        images.append(img)
    

def refreshImageFrame():
    global images
    global currentImageSlice
    global currentImage
    
    lienzo.configure( image=currentImage)



def changeImage(value):
    global currentImage
    global currentImageSlice
    global lienzo
    global figura
    global overlay

    intValue=int(float(value))
    currentImage=images[intValue]
    currentImageSlice=intValue
    img = images[currentImageSlice].copy()  
    applyOverlay(img)  # Aplica la superposición de píxeles rojos

    currentImage = ImageTk.PhotoImage(img)  # Convierte la imagen


    

    refreshImageFrame()


def applyOverlay(img):
    """Aplica la matriz overlay a la imagen actual"""
    global overlay, currentImageSlice
    
    overlay_slice = overlay[:, :, currentImageSlice]
    
    pixels = img.load()
    for y in range(overlay.shape[0]):
        for x in range(overlay.shape[1]):
            if overlay_slice[y, x] == 1:
                pixels[x, y] = (255, 0, 0)  # Rojo


def handleClick(event):
    global x_click
    global y_click
    # Obtener las coordenadas del evento
    if event.x is not None and event.y is not None:
        x_click=event.x
        y_click=event.y
        ##drawPixel(event.x, event.y)


def handleDrag(event):
    """Maneja el arrastre del mouse para seguir dibujando"""
    global x_click
    global y_click

    if x_click is not None and y_click is not None:
        drawLine(x_click, y_click, event.x, event.y)
    x_click, y_click = event.x, event.y




def drawPixel(x, y):
    """Dibuja un píxel rojo en la matriz overlay"""
    global overlay, currentImageSlice   
    if 0 <= x < overlay.shape[1] and 0 <= y < overlay.shape[0]:
        overlay[y, x, currentImageSlice] = 1  # Marcar píxel en overlay
        Draw()  # Actualizar la imagen



def drawLine(x0, y0, x1, y1):
    """Dibuja una línea entre (x0, y0) y (x1, y1) usando el algoritmo de Bresenham"""
    global overlay, currentImageSlice

    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy

    while True:
        if 0 <= x0 < overlay.shape[1] and 0 <= y0 < overlay.shape[0]:
            overlay[y0, x0, currentImageSlice] = 1  # Marcar píxel en overlay

        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy

    Draw()  # Actualizar la imagen




def process_image_data(processing_function, *args):
    """Aplica una función de procesamiento a currentFileData y actualiza la imagen."""
    global currentFileData
    newData = processing_function(currentFileData, *args)
    currentFileData = newData
    transformDataToImage()
    refreshImageFrame()



def openFile():
    global currentFileDir
    global currentFile
    currentFileDir = filedialog.askopenfilename( filetypes=(("Archivos nifti", "*.nii"),("Archivos Nifti comprimidos","*.nii.gz")))
    try:
        currentFile = nib.load(currentFileDir)
        changeFile()
    except:
        0

def saveFile():
    global currentFileData

    file_path = filedialog.asksaveasfilename(defaultextension=".nii", filetypes=[("NIfTI files", "*.nii")])
    if file_path:

        newNii= nib.Nifti1Image(np.array(currentFileData), currentFile.affine)
        nib.save(newNii, file_path)
    else:
        print('error al guardar')



def salir():
    mainWindow.destroy()
####################################################################################################################################################


### menu de control #######################################
controlMenu=tk.Menu(mainWindow)
mainWindow.config(menu=controlMenu)
menu_archivo = tk.Menu(controlMenu,tearoff=0)
controlMenu.add_cascade(label="File", menu=menu_archivo)
menu_archivo.add_command(label="Open File...", command=openFile)
menu_archivo.add_command(label="Save File", command= saveFile)
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
buttonUmbral = tk.Button(toolFrame, text="Umbralization", command=lambda: process_image_data(umbralization,128))
buttonUmbral.grid(row=1, column=0, pady=10)
buttonIsoData = tk.Button(toolFrame, text="ISOData", command=lambda: process_image_data(isoData,128))
buttonIsoData.grid(row=2, column=0, pady=10)
buttonRegionGrowing = tk.Button(toolFrame, text="Region Growing", command=lambda: process_image_data(region_growing_3d,(currentImageSlice, y_click , x_click),128))
buttonRegionGrowing.grid(row=3, column=0, pady=10)
buttonKMeans = tk.Button(toolFrame, text="K-Means", command=lambda: process_image_data(kmeans))
buttonKMeans.grid(row=0, column=0, pady=10)




##filters

buttonMeanFilter = tk.Button(toolFrame, text="Mean Filter", command=lambda: process_image_data(meanFilter))

buttonMeanFilter.grid(row=0, column=1, pady=10)
buttonMedianFilter = tk.Button(toolFrame, text="Median Filter", command=lambda: process_image_data(medianFilter))
buttonMedianFilter.grid(row=1, column=1, pady=10)
 

########################################################################

###Layout de imagen#####################################################


figura=0
lienzo=0
subplot=0
########################################################################



###Barra de slider de la imagen y rotacion##############################
##slider de imagenes
slider=ttk.Scale(viewFrame)
slider.pack()

# Lienzo donde se dibujará la imagen
lienzo = tk.Label(imageFrame)
lienzo.pack()
lienzo.bind("<Button-1>", handleClick)
lienzo.bind("<B1-Motion>", handleDrag)  # Mantener presionado y arrastrar


########################################################################

mainWindow.mainloop()