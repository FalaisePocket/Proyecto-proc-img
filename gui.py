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



mainWindow=tk.Tk()




####Es una imagen
currentFileDir=0
currentFile=0

currentFileData = 0
currentFileHeader = 0
currentImage=0
currentImageSlice=0

currentPosition=0

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
    currentImage = currentFileData[currentImageSlice]
    ###Dibujo
    slider.config(from_=0, to=currentFileData.shape[2]-1,command=changeImage)
    Draw()


def Draw():
    global lienzo
    global figura
    global subplot
    figura = Figure(figsize=(5, 4))
    subplot = figura.add_subplot(111)
    subplot.imshow(currentImage, cmap='gray', interpolation='nearest',aspect="auto")


    lienzo = FigureCanvasTkAgg(figura, master=imageFrame)
    lienzo.draw()
    lienzo.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    lienzo.mpl_connect('button_press_event', plot_listener)


def refreshImageFrame():
    subplot.clear()
    subplot.imshow(currentImage, cmap='gray', interpolation='nearest',aspect="auto")
    lienzo.draw()


def changeImage(value):
    global currentImage
    global currentImageSlice
    global lienzo
    global figura
    intValue=int(float(value))
    currentImage=currentFileData[intValue]
    currentImageSlice=intValue
    refreshImageFrame()

def plot_listener(event):
     global x_click
     global y_click
    # Obtener las coordenadas del evento
     if event.xdata is not None and event.ydata is not None:
    
        x_click = int(event.xdata)
        y_click = int(event.ydata)
    

    
def handleUmbralization():
    global currentFileData
    newData=umbralization(currentFileData,128)
    currentFileData=newData
    refreshImageFrame()
def handleISOData():
    global currentFileData
    newData=isoData(currentFileData,128)
    currentFileData=newData
    refreshImageFrame()

def handleRegionGrowing():
    global currentFileData

    newData=region_growing_3d(currentFileData,(currentImageSlice, y_click , x_click),50)
    currentFileData=newData
    refreshImageFrame()

def button_click():
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
buttonUmbral.pack(pady=20)
buttonIsoData = tk.Button(toolFrame, text="ISOData", command=handleISOData)
buttonIsoData.pack(pady=20)
buttonRegionGrowing = tk.Button(toolFrame, text="Region Growing", command=handleRegionGrowing)
buttonRegionGrowing.pack(pady=20)
buttonKMeans = tk.Button(toolFrame, text="K-Means", command=button_click)
buttonKMeans.pack(pady=20)
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