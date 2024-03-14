import tkinter as tk
from tkinter import ttk
mainWindow=tk.Tk()



currentImage=0####Es una imagen

currentColor=0##El valor del color

coordinates=[0,0]

###menu de control a lo photoshop#######################################
controlMenu=tk.Menu(mainWindow)
mainWindow.config(menu=controlMenu)

def openFile():
    print("Nyah~")

def salir():
    mainWindow.destroy()

menu_archivo = tk.Menu(controlMenu,tearoff=0)
controlMenu.add_cascade(label="File", menu=menu_archivo)
menu_archivo.add_command(label="Open File...", command=openFile)
menu_archivo.add_separator()
menu_archivo.add_command(label="Exit", command=salir)
########################################################################

###layout general#######################################################
mainFrame=tk.Frame(mainWindow)
mainFrame.pack()

toolFrame=tk.Frame(mainFrame)
imageFrame=tk.Frame(mainFrame)
viewFrame=tk.Frame(mainFrame)

toolFrame.grid(row=0, column=0, rowspan=3)
imageFrame.grid(column=1, row=0, columnspan=2, rowspan=2)
viewFrame.grid(column=1,row=2, columnspan=2)
########################################################################
###Lateral de barra de herramientas#####################################
########################################################################
###Barra de slider de la imagen y rotacion##############################
##slider de imagenes
slider=ttk.Scale(viewFrame)
slider.pack()

########################################################################







mainWindow.mainloop()