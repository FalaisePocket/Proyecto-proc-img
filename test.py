import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def plot_listener(event):
    # Obtener las coordenadas del evento
    x = event.xdata
    y = event.ydata
    if x is not None and y is not None:
        print(f"Coordenadas del clic: x={x}, y={y}")

# Crear la ventana principal
ventana_principal = tk.Tk()
ventana_principal.title("Gráfico con Listener")









# Crear un objeto Figure de Matplotlib
figura = Figure(figsize=(5, 4), dpi=100)
subplot = figura.add_subplot(111)
subplot.plot([1, 2, 3, 4, 5], [2, 3, 5, 7, 11])

# Crear un lienzo de Matplotlib para mostrar la figura en Tkinter
lienzo = FigureCanvasTkAgg(figura, master=ventana_principal)
lienzo.draw()
lienzo.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Agregar el listener al gráfico
cid = figura.canvas.mpl_connect('button_press_event', plot_listener)

# Ejecutar el bucle principal
ventana_principal.mainloop()