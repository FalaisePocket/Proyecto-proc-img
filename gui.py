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
from preprocessing.histogramMatching import histogram_matching
from preprocessing.rescaling import resize_image
from preprocessing.whiteStripe import whiteStripe
from preprocessing.zscore import zScore
from filters.meanFilter import meanFilter
from filters.medianFilter import medianFilter
from PIL import Image,ImageTk
from registro.registro import registro
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





#####Listeners####################
def changeFile():
    global currentFileData
    global currentFileHeader
    global currentImage
    global currentImageSlice
    currentFileHeader= currentFile.header
    currentFileData = currentFile.get_fdata()
    print(currentFileData)
    transformDataToImage()
    currentImage = images[currentImageSlice]

    ###Dibujo
    slider.config(from_=0, to=currentFileData.shape[2]-1,command=changeImage)
    
    Draw()


def Draw():
    global lienzo
    global figura
    global subplot
    global images
    global currentImageSlice
    global imageFrame

    
    lienzo = tk.Label(imageFrame, image=images[currentImageSlice])
    lienzo.pack( side=tk.TOP, fill=tk.BOTH, expand=1 )
    lienzo.bind("<Button-1>",handleClick)
    



def transformDataToImage():
    global currentFileData
    global images
    images=[]
    for slices in currentFileData:
        img= Image.fromarray(slices) 
        newimg= ImageTk.PhotoImage(img)
        images.append(newimg)

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

    intValue=int(float(value))
    currentImage=images[intValue]
    currentImageSlice=intValue

    refreshImageFrame()

def handleClick(event):
    global x_click
    global y_click
    # Obtener las coordenadas del evento
    if event.x is not None and event.y is not None:
    
        x_click = int(event.x)
        y_click = int(event.y)

    print(x_click)
    print(y_click)

    
def handleUmbralization():
    global currentFileData
    newData=umbralization(currentFileData,128)
    currentFileData=newData
    transformDataToImage()
    refreshImageFrame()


def handleISOData():
    global currentFileData
    newData=isoData(currentFileData,128)
    currentFileData=newData
    transformDataToImage()
    refreshImageFrame()

def handleRegionGrowing():
    global currentFileData

    newData=region_growing_3d(currentFileData,(currentImageSlice, y_click , x_click),128)
    currentFileData=newData
    transformDataToImage()
    refreshImageFrame()

def handleHistogramMatching():
    global currentFileData
    newData=histogram_matching(currentFileData)
    currentFileData=newData
    transformDataToImage()
    refreshImageFrame()


def handleRescaling():
    global currentFileData
    newData= resize_image(currentFileData)
    currentFileData=newData
    transformDataToImage()
    refreshImageFrame()


def handleWhiteStripe():
    global currentFileData  
    newData= whiteStripe(currentFileData)
    currentFileData = newData
    transformDataToImage()
    refreshImageFrame()

def handleZScore():
    global currentFileData
    newData=zScore(currentFileData)
    currentFileData=newData
    transformDataToImage()
    refreshImageFrame()

def handleMeanFilter():
    global currentFileData
    newData=meanFilter(currentFileData)
    currentFileData=newData
    transformDataToImage()
    refreshImageFrame()

def handleMedianFilter():
    global currentFileData
    newData=medianFilter(currentFileData)
    currentFileData=newData
    transformDataToImage()
    refreshImageFrame()

def handleRegistration():
    global currentFileDir
    registro(currentFileDir)


def handleKMeans():
    global currentFileData
    newData=kmeans(currentFileData)
    currentFileData=newData
    transformDataToImage()
    refreshImageFrame()


def button_click():
    global currentFileData
    print('...')


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


###menu de control a lo photoshop#######################################
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
buttonUmbral = tk.Button(toolFrame, text="Umbralization", command=handleUmbralization)
buttonUmbral.grid(row=1, column=0, pady=10)
buttonIsoData = tk.Button(toolFrame, text="ISOData", command=handleISOData)
buttonIsoData.grid(row=2, column=0, pady=10)
buttonRegionGrowing = tk.Button(toolFrame, text="Region Growing", command=handleRegionGrowing)
buttonRegionGrowing.grid(row=3, column=0, pady=10)
buttonKMeans = tk.Button(toolFrame, text="K-Means", command=handleKMeans)
buttonKMeans.grid(row=0, column=0, pady=10)



##normalizacion
buttonhistogram = tk.Button(toolFrame, text="Histogram Matching", command=handleHistogramMatching)
buttonhistogram.grid(row=4, column=0, pady=10)
buttonrescaling = tk.Button(toolFrame, text="Rescaling", command=handleRescaling)
buttonrescaling.grid(row=0, column=1, pady=10)
buttonwhitestripe = tk.Button(toolFrame, text="White Stripe", command=handleWhiteStripe)
buttonwhitestripe.grid(row=1, column=1, pady=10)
buttonzscore = tk.Button(toolFrame, text="Z-Score", command=handleZScore)
buttonzscore.grid(row=2, column=1, pady=10)

##filters
buttonMeanFilter = tk.Button(toolFrame, text="Mean Filter", command=handleMeanFilter)
buttonMeanFilter.grid(row=3, column=1, pady=10)
buttonMedianFilter = tk.Button(toolFrame, text="Median Filter", command=handleMedianFilter)
buttonMedianFilter.grid(row=4, column=1, pady=10)

buttonRegistration = tk.Button(toolFrame, text="Registration", command=handleRegistration)
buttonRegistration.grid(row=5, column=0, pady=10)  

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

########################################################################

mainWindow.mainloop()