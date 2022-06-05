from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
def setearForms():
    nombre.set("")
    apellido.set("")
    dni.set(0)
    habitacion.set(0)
    fechaIngreso.set("")
    fechaSalida.set("")
    
def accionBoton():
    if (botonVariable.get()=="Guardar"):
        print("Nombre :",nombre.get(),"Apellido :",apellido.get(),"DNI :",dni.get(),"Habitacion :",habitacion.get(),"Fecha de Ingreso :",fechaIngreso.get(),"Fecha de Salida :",fechaSalida.get())
    else:
        print("actualizar")
    
    setearForms()

root = Tk()
root.title("Hotel Teressitta")

#Variables
nombre=StringVar()
apellido=StringVar()
dni=IntVar()
habitacion=IntVar()
fechaIngreso=StringVar()
fechaSalida=StringVar()
botonVariable=StringVar()
botonVariable.set("Guardar")

#Se declaran los Frames
marco = ttk.Frame(root, padding=10)
formulario = ttk.LabelFrame(marco,text="Formulario cliente",padding=10)
listaDatos = ttk.LabelFrame(marco,text="Lista de clientes",padding=10)
herramientas = ttk.LabelFrame(marco,text="Herramientas",padding=10)

#formularios
formularioNombre = ttk.Entry(formulario,textvariable=nombre)
formularioApellido = ttk.Entry(formulario,textvariable=apellido)
formularioDNI =ttk.Entry(formulario,textvariable=dni)
formularioHabitacion = ttk.Entry(formulario,textvariable=habitacion)
formularioFechaIngreso = DateEntry(formulario,selectmode="dia",textvariable=fechaIngreso)
formularioFechaSalida = DateEntry(formulario,selectmode="dia",textvariable=fechaSalida)

#botones
botonAccion=ttk.Button(formulario,textvariable=botonVariable,padding= ("10 5 10 5"),command=accionBoton)
botonCrear=ttk.Button(herramientas,text="Crear",padding= ("10 5 10 5"))
botonActualizar= ttk.Button(herramientas,text="Actualizar",padding= ("10 5 10 5"))
botonEliminar= ttk.Button(herramientas,text="Eliminar",padding= ("10 5 10 5"))

# etiquetas
etiquetaNombre = ttk.Label(formulario,text="Nombre")
etiquetaApellido = ttk.Label(formulario,text="Apellido")
etiquetaDNI = ttk.Label(formulario,text="DNI")
etiquetaHabitacion = ttk.Label(formulario,text="Habitacion")
etiquetaFechaIngreso = ttk.Label(formulario,text="Fecha de Ingreso")
etiquetaFechaSalida = ttk.Label(formulario, text="Fechas de salida")

# se empaquetan los elementos
marco.grid(column=0, row=0,sticky=(N,S,E,W))
formulario.grid(column=0, row=0)
listaDatos.grid(column=0, row=1)
herramientas.grid(column=0, row=2)

etiquetaNombre.grid(column=0, row =0,sticky=SW, padx=5)
formularioNombre.grid(column=0, row=1, sticky=(W), padx=5)

etiquetaApellido.grid(column=1, row =0, sticky=W, padx=5)
formularioApellido.grid(column=1, row=1, sticky=(W),padx=5)

etiquetaDNI.grid(column=2, row =0,sticky=W,padx=5)
formularioDNI.grid(column=2, row=1, sticky=(W),padx=5)

etiquetaHabitacion.grid(column=3, row =0,sticky=W,padx=5)
formularioHabitacion.grid(column=3, row=1,sticky=(W), padx=5)

etiquetaFechaIngreso.grid(column=4, row =0,sticky=W,padx=5)
formularioFechaIngreso.grid(column=4, row=1,sticky=(W), padx=5)

etiquetaFechaSalida.grid(column=5, row =0,sticky=W,padx=5)
formularioFechaSalida.grid(column=5, row=1,sticky=(W),padx=5)

botonAccion.grid(column=5,row=2,sticky=W,pady=10)
botonCrear.grid(column=0,row=0,sticky=W,padx=20)
botonActualizar.grid(column=1, row=0,sticky=W,padx=20)
botonEliminar.grid(column=2,row=0,sticky=W,padx=20)

# Lista de clientes
arbol=ttk.Treeview(listaDatos,columns=6,)
arbol['columns'] =('nombre','apellido','DNI','habitacion','fecha ingreso','fecha salida')

arbol.grid(column=0,row=0)
arbol.column('#0',width=40,minwidth=10)
arbol.heading("#0",text='No')

arbol.column('nombre',width=120,minwidth=10)
arbol.heading('nombre',text='Nombre')

arbol.column('apellido',width=120,minwidth=10)
arbol.heading('apellido',text='Apellido')

arbol.column('DNI',width=100,minwidth=10)
arbol.heading('DNI',text='DNI')

arbol.column('habitacion',width=100,minwidth=10)
arbol.heading('habitacion',text='Habitacion')

arbol.column('fecha ingreso',width=100,minwidth=10)
arbol.heading('fecha ingreso',text='Fecha ingreso')

arbol.column('fecha salida',width=100,minwidth=10)
arbol.heading('fecha salida',text='Fecha Salida')

root.mainloop()