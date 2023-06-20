try:
    import tkinter as tk
    import importlib
    import subprocess
    from tkinter import filedialog
    from tkinter import ttk,Tk,Label,Frame
    import pandas as pd
    import matplotlib.pyplot as plt
    from tkcalendar import  DateEntry
    import os.path
    import seaborn as sns
    from PIL import ImageTk,Image
except ModuleNotFoundError:
# Este código permite analizar si las librerias de la lista estan instaladas, si no, las instala.
  required_packages = ['pandas','matplotlib','seaborn','tkinter','os','PIL']
  for packages in required_packages:
    try:
        importlib.import_module(packages)
        print(f"{packages} esta instalado")
    except ImportError:
        print(f"{packages} no esta instalado, se procede a instalar...")
        subprocess.check_call(['pip', 'install', packages])

# Incorporar Iconos de Forma ordenada

def incorporar_iconos():
    ruta = os.getcwd()
    cambiar_directorio = os.chdir(f'{ruta}\ICONOS')
    ruta1 = os.getcwd()
    lista_iconos = os.listdir(ruta1)
    return lista_iconos      

# Crear ventana principal
ventana = tk.Tk()
ventana.title("Interfaz Gráfica")
ancho_pantalla = ventana.winfo_screenwidth()
alto_pantalla = ventana.winfo_screenheight()
ventana.geometry(f"{ventana.winfo_screenwidth()}x{ventana.winfo_screenheight()}+0+0")
ventana.title("Tangara 1.0 ITM 2023")


# Definir funciones
def cargar_archivo():
    archivo = filedialog.askopenfilename(filetypes=[("Archivo Excel", ".xlsx"),("Archivo Excel", ".csv")])
    entrada_archivo.delete(0, tk.END)
    entrada_archivo.insert(0, archivo)

    
def cargar():
    archivo = entrada_archivo.get()
    if archivo != '':
        try:
            nombre , extension = os.path.splitext(archivo)
            if extension == '.csv':
                df = pd.read_csv(archivo, delimiter=(";"))
            elif extension == '.xlsx':
                df = pd.read_excel(archivo)

            opciones_columnas['values'] = list(df.columns)
            opciones_id['values'] = list(df['id'].unique())
            textbox.delete('1.0', tk.END)
        except Exception as e:
            tk.messagebox.showerror("Error", "No se pudo leer el archivo. Detalle: " + str(e))
    else:
        tk.messagebox.showwarning("Advertencia", "Debes seleccionar un archivo primero.")

def filtrar():
    archivo = entrada_archivo.get()
    filtro = valor_menu_id.get()
    if archivo != '':
        try:
            nombre , extension = os.path.splitext(archivo)
            if extension == '.csv':
                df = pd.read_csv(archivo, delimiter=(";"))
            elif extension == '.xlsx':
                df = pd.read_excel(archivo)
            
            if df['id'].value_counts().values.shape[0] == 1:
                df = df
            else:
                df = df[df['id'] == filtro]


            opciones_columnas['values'] = ['Masa corporal', 'Agua corporal', 'Masa musculo esqueletico']
            opciones_id['values'] = list(df['id'].unique())
            textbox.delete('1.0', tk.END)
            textbox.insert(tk.END, str(df['timestamp']))
        except Exception as e:
            tk.messagebox.showerror("Error", "No se pudo leer el archivo. Detalle: " + str(e))
    else:
        tk.messagebox.showwarning("Advertencia", "Debes seleccionar un archivo primero.")
        

def graficar():
    archivo = entrada_archivo.get()
    columna = valor_menu.get()
    filtro = valor_menu_id.get()
    if archivo != '':
        try:
            nombre , extension = os.path.splitext(archivo)
            if extension == '.csv':
                df = pd.read_csv(archivo, delimiter=(";"))
            elif extension == '.xlsx':
                df = pd.read_excel(archivo)


            if df['id'].value_counts().values.shape[0] == 1:
                df = df
            else:
                df = df[df['id'] == filtro]
            df['Absolute fat mass value'] = df['Absolute fat mass value'].astype('float64')
            df['Fat-free mass value'] = df['Fat-free mass value'].astype('float64')
            df['Total Body Water value'] = df['Total Body Water value'].astype('float64')
            df['Extracellular water value'] = df['Extracellular water value'].astype('float64')
            df['Skeletal muscle mass value'] = df['Skeletal muscle mass value'].astype('float64')
            df['SMM (torso) value'] = df['SMM (torso) value'].astype('float64')
            df['SMM (RA) value'] = df['SMM (RA) value'].astype('float64')
            df['SMM (RL) value'] = df['SMM (RL) value'].astype('float64')
            df['SMM (LL) value'] = df['SMM (LL) value'].astype('float64')
            df['SMM (LA) value'] = df['SMM (LA) value'].astype('float64')
            df ['Relative fat mass value'] = df ['Relative fat mass value'].astype('float64')
            
            if columna == 'Masa corporal':
                x  =df['timestamp'][:len(df['timestamp'])+1]
                y =  df['Skeletal muscle mass value'][:len(df['Skeletal muscle mass value'])+1]
                y1 = df ['Relative fat mass value'][:len( df ['Relative fat mass value'])+1]
                fig = plt.figure(figsize = (12,5))
                ax = fig.gca()
                plt.plot(x,y,linestyle = '--', marker = 'o',color = '#6A9796', label ='Masa magra')
                plt.plot(x,y1,linestyle = '--', marker = 'o',color = '#324848', label = 'Masa grasa')
                plt.axvspan(0,1.3,facecolor='blue',alpha=0.3)
                plt.axvspan(1.3,2.6,facecolor='green',alpha=0.3)
                plt.axvspan(2.6,4,facecolor='red',alpha=0.3)
                plt.title('Masa corporal')
                plt.xlabel('Tiempo(dias)')
                plt.ylabel('Kg')
                plt.legend(loc ='best')
                plt.grid(axis='y')
                plt.show()
            elif columna == 'Agua corporal':
                x  =df['timestamp'][:len(df['timestamp'])+1]
                y =  df['Total Body Water value'][:len(df['Total Body Water value'])+1]
                y1 = df ['Extracellular water value'][:len(df ['Extracellular water value'])+1]
                fig = plt.figure(figsize = (12,5))
                ax = fig.gca()
                plt.plot(x,y,linestyle = '--', marker = 'o',color = '#6A9796', label ='Agua total corporal')
                plt.plot(x,y1,linestyle = '--', marker = 'o',color = '#324848', label = 'Agua extracelular')
                plt.axvspan(0,1.3,facecolor='blue',alpha=0.3)
                plt.axvspan(1.3,2.6,facecolor='green',alpha=0.3)
                plt.axvspan(2.6,4,facecolor='red',alpha=0.3)
                plt.xlabel('Tiempo(dias)')
                plt.ylabel('Litros')
                plt.title('Agua corporal')
                plt.legend(loc ='best')
                plt.grid(axis='y')
                plt.show()

            elif columna == 'Masa musculo esqueletico':
                x  =df['timestamp'][:len(df['timestamp'])+1]
                y1 =  df['Skeletal muscle mass value'][:len(df['Skeletal muscle mass value'])+1]
                y2 = df ['SMM (torso) value'][:len(df ['SMM (torso) value'])+1]
                y3 = df ['SMM (RA) value'][:len(df ['SMM (RA) value'])+1]
                y4 = df ['SMM (RL) value'][:len(df ['SMM (RL) value'])+1]
                y5 = df ['SMM (LL) value'][:len(df ['SMM (LL) value'])+1]
                y6 = df ['SMM (LA) value'][:len(df ['SMM (LA) value'])+1]
                
                fig = plt.figure(figsize = (12,5))
                ax = fig.gca()
                plt.plot(x,y1,linestyle = '--', marker = 'o',color = '#6A9796', label ='Masa muscular esquelética')
                plt.plot(x,y2,linestyle = '--', marker = 'o',color = '#324848', label = 'Torso')
                plt.plot(x,y3,linestyle = '--', marker = 'o',color = 'blue', label = 'Brazo derecho')
                plt.plot(x,y4,linestyle = '--', marker = 'o',color = 'red', label = 'Pierna derecha')
                plt.plot(x,y5,linestyle = '--', marker = 'o',color = 'yellow', label = 'Pierna izquierda')
                plt.plot(x,y6,linestyle = '--', marker = 'o',color = 'green', label = 'Brazo izquierdo')
                plt.axvspan(0,1.3,facecolor='blue',alpha=0.3)
                plt.axvspan(1.3,2.6,facecolor='green',alpha=0.3)
                plt.axvspan(2.6,4,facecolor='red',alpha=0.3)
                plt.xlabel('Tiempo(dias)')
                plt.ylabel('Kg')
                plt.title('Masa muscular esquelética')
                plt.legend(loc ='best')
                plt.grid(axis='y')
                plt.show()


        except Exception as e:
            tk.messagebox.showerror("Error", "No se pudo leer el archivo o la columna no existe. Detalle: " + str(e))
    else:
        tk.messagebox.showwarning("Advertencia", "Debes seleccionar un archivo primero.")






# Crear widgets
etiqueta1 = tk.Label(ventana, text="Seleccione archivo puente:")
etiqueta2 = tk.Label(ventana, text="Seleccione al sujeto:")
etiqueta3 = tk.Label(ventana, text="Seleccione el tipo de gráfico:")
etiqueta4 = tk.Label(ventana, text="")
etiqueta5 = tk.Label(ventana, text="Dirección del archivo:")
etiqueta6 = tk.Label(ventana, text="Muestre los datos disponibles:")
etiqueta7 = tk.Label(ventana, text="Datos disponibles: ")

#etiquetas
etiqueta1.grid(row=0, column=0)
etiqueta2.grid(row=1, column=0)
etiqueta3.grid(row=2, column=0)
etiqueta4.grid(row=4)
etiqueta5.grid(row=0, column=2)
etiqueta6.grid(row=1, column=2)
etiqueta7.grid(row=4, column=1)

#botones
boton_seleccionar_archivo = tk.Button(ventana, text="Aquí", command=cargar_archivo)
boton_cargar = tk.Button(ventana, text="Cargar archivo", command=cargar)
boton_graficar = tk.Button(ventana, text="Ver gráfico", command=graficar)
boton_mostrar_contenido = tk.Button(ventana, text="Aquí", command=filtrar)

boton_seleccionar_archivo.grid(row=0, column=1)
boton_graficar.grid(row=3, column=2)
boton_mostrar_contenido.grid(row=1, column=3)
boton_cargar.grid(row=0, column=4)

#Entradas
entrada_archivo = tk.Entry(ventana)
valor_menu = tk.StringVar()
valor_menu_id = tk.StringVar()
opciones_columnas = ttk.Combobox(ventana, textvariable=valor_menu)
opciones_id = ttk.Combobox(ventana, textvariable=valor_menu_id)
textbox = tk.Text(ventana,height=80 , width=170)

entrada_archivo.grid(row=0, column=3)
opciones_id.grid(row=1, column=1)
opciones_columnas.grid(row=2, column=1)



textbox.grid(row=6, column=1, columnspan=10)

# Añadir imagen de itm
lista = incorporar_iconos()
imagen = Image.open(lista[1])
imagen_tk = ImageTk.PhotoImage(imagen)
frame_imagen = Frame(ventana)
frame_imagen.grid(row = 0,column= 5)
etiqueta_img = Label(frame_imagen, image =imagen_tk).pack()
#Iconos
icono = Image.open(lista[0])
icono_mostrar = ImageTk.PhotoImage(icono)
ventana.wm_iconphoto(True,icono_mostrar)
# Ejecutar ventana principal
ventana.mainloop()