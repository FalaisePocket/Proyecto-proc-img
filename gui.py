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
from preprocessing.histogramMatching import histogram_matching
from preprocessing.rescaling import resize_image
from preprocessing.whiteStripe import whiteStripe
from preprocessing.zscore import zScore
from registro.registro import registro
from laplacian.segmentationTwo import laplacian_segmentation

mainWindow=tk.Tk()



####Es una imagen
currentFileDir=0
currentFile=0

currentFileData = 0
currentFileHeader = 0

currentImage=0
currentImageSlice=0

currentPosition=0

#rotacion de la imagen
s_i=''
a_p=''
r_l=''


images=[]

##El valor del color
currentColor=0

y_click=0
x_click=0

overlay = None

currentButton = None


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
    overlay = np.zeros_like(currentFileData, dtype=np.int8)
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


'''def applyOverlay(img):
    """Aplica la matriz overlay a la imagen actual"""
    global overlay, currentImageSlice
    
    overlay_slice = overlay[:, :, currentImageSlice]
    
    pixels = img.load()
    for y in range(overlay.shape[0]):
        for x in range(overlay.shape[1]):
            if overlay_slice[y, x] == 1:
                pixels[x, y] = (255, 0, 0)  # Rojo'''
def applyOverlay(img):
    global overlay, currentImageSlice
    overlay_slice = overlay[:, :, currentImageSlice]
    pixels = img.load()
    for y in range(overlay.shape[0]):
        for x in range(overlay.shape[1]):
            if overlay_slice[y, x] == 1:
                pixels[x, y] = (255, 0, 0)  # Rojo
            elif overlay_slice[y, x] == -1:
                pixels[x, y] = (0, 255, 0)  # Verde

'''
def handleClick(event):
    global x_click
    global y_click
    # Obtener las coordenadas del evento
    if event.x is not None and event.y is not None:
        x_click=event.x
        y_click=event.y
        ##drawPixel(event.x, event.y)'''
def handleClick(event):
    global x_click, y_click, currentButton
    currentButton = event.num

    # CORRECCIÓN: Verificar que la imagen existe
    if not images or currentImageSlice >= len(images):
        return
        
    img_w, img_h = images[currentImageSlice].size
    widget_w = lienzo.winfo_width()
    widget_h = lienzo.winfo_height()
    
    # CORRECCIÓN: Verificar divisiones por cero
    if widget_w <= 0 or widget_h <= 0:
        return

    scale_x = img_w / widget_w
    scale_y = img_h / widget_h

    x_img = int(event.x * scale_x)
    y_img = int(event.y * scale_y)
    
    # CORRECCIÓN: Verificar límites antes de asignar
    if x_img < 0 or x_img >= img_w or y_img < 0 or y_img >= img_h:
        return

    x_click, y_click = x_img, y_img

    print(f"Click en: widget({event.x}, {event.y}) -> imagen({x_img}, {y_img})")  # DEBUG
    
    if currentButton == 1:
        drawPixel(x_img, y_img, value=1)
    elif currentButton == 3:
        drawPixel(x_img, y_img, value=-1)

'''
def handleDrag(event):
    """Maneja el arrastre del mouse para seguir dibujando"""
    global x_click
    global y_click

    if x_click is not None and y_click is not None:
        drawLine(x_click, y_click, event.x, event.y)
    x_click, y_click = event.x, event.y'''

def handleDrag(event):
    global x_click, y_click, currentButton
    if currentButton is None or x_click is None or y_click is None:
        return
        
    # CORRECCIÓN: Verificar que la imagen existe
    if not images or currentImageSlice >= len(images):
        return

    img_w, img_h = images[currentImageSlice].size
    widget_w = lienzo.winfo_width()
    widget_h = lienzo.winfo_height()
    
    # CORRECCIÓN: Verificar divisiones por cero
    if widget_w <= 0 or widget_h <= 0:
        return

    scale_x = img_w / widget_w
    scale_y = img_h / widget_h

    x_img = int(event.x * scale_x)
    y_img = int(event.y * scale_y)
    
    # CORRECCIÓN: Verificar límites
    if x_img < 0 or x_img >= img_w or y_img < 0 or y_img >= img_h:
        return

    value = 1 if currentButton == 1 else -1
    drawLine(x_click, y_click, x_img, y_img, value=value)

    x_click, y_click = x_img, y_img

def handleRelease(event):
    global currentButton
    currentButton = None



def drawPixel(x, y, value=1):
    """Dibuja un píxel en la matriz overlay"""
    global overlay, currentImageSlice
    
    print(f"Imagen PIL size: {images[currentImageSlice].size}")
    print(f"Overlay shape: {overlay.shape}")
    print(f"currentFileData shape: {currentFileData.shape}")
    
    # CORRECCIÓN: Verificar límites correctamente
    if (0 <= x < overlay.shape[1] and 
        0 <= y < overlay.shape[0] and 
        0 <= currentImageSlice < overlay.shape[2]):
        
        overlay[y, x, currentImageSlice] = value
        print(f"Píxel guardado. Valor en overlay[{y}, {x}, {currentImageSlice}] = {overlay[y, x, currentImageSlice]}")  # DEBUG
        Draw()
    else:
        print(f"Coordenadas fuera de límites: x={x}, y={y}, slice={currentImageSlice}")  # DEBUG

'''

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
'''
def drawLine(x0, y0, x1, y1, value=1):
    global overlay, currentImageSlice
    
    print(f"drawLine: ({x0}, {y0}) -> ({x1}, {y1}) = {value}")  # DEBUG

    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy

    while True:
        # CORRECCIÓN: Verificar límites en cada píxel
        if (0 <= x0 < overlay.shape[1] and 
            0 <= y0 < overlay.shape[0] and 
            0 <= currentImageSlice < overlay.shape[2]):
            overlay[y0, x0, currentImageSlice] = value

        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy

    Draw()

def debug_overlay():
    global overlay, currentImageSlice
    if overlay is not None:
        slice_data = overlay[:, :, currentImageSlice]
        unique_values = np.unique(slice_data)
        print(f"Slice {currentImageSlice} - Valores únicos en overlay: {unique_values}")
        if len(unique_values) > 1:
            for val in unique_values:
                if val != 0:
                    count = np.sum(slice_data == val)
                    print(f"  Valor {val}: {count} píxeles")

def process_image_data(processing_function, *args):
    """Aplica una función de procesamiento a currentFileData y actualiza la imagen."""
    global currentFileData
    newData = processing_function(currentFileData, *args)
    currentFileData = newData
    transformDataToImage()
    refreshImageFrame()

def apply_registration(moving_path):
    global currentFileData, currentFile, overlay
    registro(moving_path)
    
    # Cargar imagen registrada
    registered_img = nib.load('imagen_movil_registrada.nii')
    currentFile = registered_img
    currentFileData = registered_img.get_fdata()
    # CORRECCIÓN: Usar int8 consistentemente
    overlay = np.zeros_like(currentFileData, dtype=np.int8)
    transformDataToImage()
    refreshImageFrame()
    Draw()




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


def rotate(axis,param,value):
    global overlay, currentFile
    newOrient=[r_l,a_p,s_i]
    reoriented_img = currentFile.as_reoriented(nib.orientations.axcodes2ornt(newOrient))
    currentFile=reoriented_img
    changeFile()
    Draw()


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


##Normalización

buttonhistogram = tk.Button(toolFrame, text="Histogram Matching", command=lambda: process_image_data(histogram_matching))
buttonhistogram.grid(row=4, column=0, pady=10)
buttonrescaling = tk.Button(toolFrame, text="Rescaling", command=lambda: process_image_data(resize_image))
buttonrescaling.grid(row=0, column=1, pady=10)
buttonwhitestripe = tk.Button(toolFrame, text="White Stripe", command=lambda: process_image_data(whiteStripe))
buttonwhitestripe.grid(row=1, column=1, pady=10)
buttonzscore = tk.Button(toolFrame, text="Z-Score", command=lambda: process_image_data(zScore))
buttonzscore.grid(row=2, column=1, pady=10)


##filters

buttonMeanFilter = tk.Button(toolFrame, text="Mean Filter", command=lambda: process_image_data(meanFilter))

buttonMeanFilter.grid(row=0, column=1, pady=10)
buttonMedianFilter = tk.Button(toolFrame, text="Median Filter", command=lambda: process_image_data(medianFilter))
buttonMedianFilter.grid(row=1, column=1, pady=10)
 

########################################################################

###Registro###############################################

buttonRegistration = tk.Button(toolFrame, text="Registration", command=lambda: apply_registration(currentFileDir))
buttonRegistration.grid(row=5, column=0, pady=10) 


#########Laplacian###############

def handleLaplacian():
    global currentFileData, overlay, currentImageSlice
    
    print(f"=== DEBUG LAPLACIAN ===")
    print(f"Current slice: {currentImageSlice}")
    print(f"Overlay shape: {overlay.shape}")
    
    # Verificar si hay semillas en el slice actual
    current_slice_overlay = overlay[:, :, currentImageSlice]
    unique_vals = np.unique(current_slice_overlay)
    print(f"Valores únicos en overlay slice {currentImageSlice}: {unique_vals}")
    
    for val in unique_vals:
        if val != 0:
            positions = np.where(current_slice_overlay == val)
            print(f"Valor {val}: {len(positions[0])} píxeles")
            if len(positions[0]) > 0:
                print(f"  Primeras 5 posiciones: {list(zip(positions[0][:5], positions[1][:5]))}")

'''
def handleLaplacian():
    
    global currentFileData,overlay, currentImageSlice

    for line in overlay[currentImageSlice]:
        print(line)
    seeds = overlay[currentImageSlice]
    newSlice = laplacian_segmentation(currentFileData[currentImageSlice], seeds)
    currentFileData[currentImageSlice]=newSlice

    print("Semillas:", np.unique(overlay, return_counts=True))
    print("Intensidades:", currentFileData.min(), currentFileData.max())
    print("Resultado:", np.unique(newSlice, return_counts=True))

    #newData = processing_function(currentFileData, *args)
    ##currentFileData = newData
    
    transformDataToImage()
    refreshImageFrame()'''

def handleLaplacian():
    global currentFileData, overlay, currentImageSlice
    
    print(f"=== PROCESANDO LAPLACIAN ===")
    print(f"Slice actual: {currentImageSlice}")
    
    # Obtener el slice actual del overlay (semillas)
    current_slice_overlay = overlay[:, :, currentImageSlice]
    
    # Obtener el slice actual de la imagen
    current_image_slice = currentFileData[:, :, currentImageSlice].copy()
    
    # Verificar que tenemos semillas
    unique_vals = np.unique(current_slice_overlay)
    has_positive = np.any(current_slice_overlay == 1)
    has_negative = np.any(current_slice_overlay == -1)
    
    print(f"Semillas en slice {currentImageSlice}: {unique_vals}")
    print(f"Píxeles positivos: {np.sum(current_slice_overlay == 1)}")
    print(f"Píxeles negativos: {np.sum(current_slice_overlay == -1)}")
    
    if not (has_positive and has_negative):
        print("ERROR: Necesitas marcar tanto píxeles POSITIVOS (click izquierdo) como NEGATIVOS (click derecho)")
        return
    
    print(f"Imagen slice shape: {current_image_slice.shape}")
    print(f"Overlay slice shape: {current_slice_overlay.shape}")
    print(f"Intensidades originales: {current_image_slice.min():.2f} - {current_image_slice.max():.2f}")
    
    try:
        # Llamar a la función laplacian_segmentation con el slice actual
        print("Ejecutando segmentación Laplaciana...")
        segmented_slice = laplacian_segmentation(current_image_slice, current_slice_overlay)
        
        # REEMPLAZAR el slice en currentFileData
        currentFileData[:, :, currentImageSlice] = segmented_slice
        
        print("✅ Segmentación completada exitosamente")
        print(f"Resultado shape: {segmented_slice.shape}")
        print(f"Intensidades resultado: {segmented_slice.min():.2f} - {segmented_slice.max():.2f}")
        print(f"Valores únicos: {np.unique(segmented_slice)}")
        
        # Actualizar la visualización en pantalla
        transformDataToImage()  # Regenera todas las imágenes PIL
        currentImage = images[currentImageSlice]  # Actualiza la imagen actual
        Draw()  # Redibuja en pantalla
        
        print("✅ Visualización actualizada")
        
        # Limpiar las semillas del slice actual (opcional)
        # overlay[:, :, currentImageSlice] = 0
        
    except Exception as e:
        print(f"❌ ERROR en segmentación: {e}")
        import traceback
        traceback.print_exc()



buttonLaplacian= tk.Button(toolFrame,text="Laplacian", command=handleLaplacian)
buttonLaplacian.grid(row=3, column=1, pady=10)

#################
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

lienzo.bind("<Button-3>", handleClick)        # Click derecho
lienzo.bind("<B3-Motion>", handleDrag)        # Arrastrar con botón derecho

lienzo.bind("<ButtonRelease-1>", handleRelease)
lienzo.bind("<ButtonRelease-3>", handleRelease)


########################################################################

mainWindow.mainloop()