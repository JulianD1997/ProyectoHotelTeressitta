import sqlite3
from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import datetime
import traceback

# funciones
def conexionSQL(consulta, parametros=()):
    miConexion = sqlite3.connect("HotelTeressitta")
    cursor = miConexion.cursor()
    try:
        cursor.execute(consulta, parametros)
        return cursor.fetchall()
    except Exception:
        traceback.print_exc()
    finally:
        miConexion.commit()

def crearTabla():
    consulta = ('''--sql
        CREATE TABLE Clientes(
            ID  INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            nombre VARCHAR(75),
            apellido VARCHAR(75),
            DNI INTEGER(15) UNIQUE NOT NULL,
            habitacion INTEGER(6) UNIQUE NOT NULL,
            fechaDeIngreso DATE NOT NULL,
            fechaDESalida DATE NOT NULL
        );'''
                )
    conexionSQL(consulta)

def validarDatos():
    print(len(nombre.get())!=0 and len(apellido.get())!=0 and dni.get()!=0 and habitacion.get()!=0)
    return len(nombre.get())!=0 and len(apellido.get())!=0 and dni.get()!=0 and habitacion.get()!=0

def crearCliente():
    if validarDatos():
        consulta = """--sql
            INSERT INTO Clientes
            values(NULL,?,?,?,?,?,?);
        """
        ingreso = datetime.strptime(fechaIngreso.get(), '%d/%m/%y').date()
        salida = datetime.strptime(fechaIngreso.get(), '%d/%m/%y').date()
        
        parametros = (nombre.get(), apellido.get(), dni.get(), habitacion.get(),ingreso,salida)
        conexionSQL(consulta,parametros)
        print("Cliente guardado correctamente")
    else:
        print("todos los datos son requeridos")
    leerCliente()

def leerCliente():
    #se borrar los clientes del arbol
    clientes= arbol.get_children()
    for cliente in clientes:
        arbol.delete(cliente)
    
    consulta= ("""--sql
        SELECT * FROM Clientes ORDER BY apellido ASC;
    """)
    datos=conexionSQL(consulta)
    print(datos)
    for cliente in datos:
        arbol.insert("","end",text=cliente[3],values=(cliente[1],cliente[2],cliente[4],cliente[5],cliente[6]))
    
def modificarCliente():
    if validarDatos :
        consulta = """--sql
            UPDATE Clientes
            SET nombre = ?,
                apellido = ?, 
                DNI = ?,
                habitacion = ?,
                fechaDeIngreso = ?,
                fechaDeSalida = ?,
            where DNI= ?;
        """
        ingreso = datetime.strptime(fechaIngreso.get(), "%d/%m/%y").date()
        salida = datetime.strptime(fechaIngreso.get(), "%d/%m/%y").date()

        parametros = (nombre.get(), apellido.get(), dni.get(), habitacion.get(),ingreso,salida)
        conexionSQL(consulta,parametros)
        leerCliente()
    else:
        print("Todos los datos deben ser ingresados")

def borrarCliente():
    consulta= """--sql
        DELETE FROM Clientes
        WHERE DNI=?;
    """
    parametros=()
    conexionSQL(consulta, parametros)
    leerCliente()

def setearForms():
    nombre.set("")
    apellido.set("")
    dni.set(0)
    habitacion.set(0)
    hoy = datetime.today().date()
    fecha=str(hoy.strftime('%d/%m/%y'))
    fechaIngreso.set(fecha)
    fechaSalida.set(fecha)

def accionBoton():

    if (botonVariable.get() == "Guardar"):
        crearCliente()
    else:
        modificarCliente()

    botonVariable.set("Guardar")
    setearForms()

root = Tk()
root.title("Hotel Teressitta")

# Variables
crearTabla()
nombre = StringVar()
apellido = StringVar()
dni = IntVar()
habitacion = IntVar()
fechaIngreso = StringVar()
fechaSalida = StringVar()
botonVariable = StringVar()
botonVariable.set("Guardar")

# Se declaran los Frames
marco = ttk.Frame(root, padding=10)
formulario = ttk.LabelFrame(
    marco, height=700, text="Formulario cliente", padding=10)
listaDatos = ttk.LabelFrame(
    marco, height=700, text="Lista de clientes", padding=10)
herramientas = ttk.LabelFrame(
    marco, height=700, text="Herramientas", padding=10)

# formularios
formularioNombre = ttk.Entry(formulario, textvariable=nombre)
formularioApellido = ttk.Entry(formulario, textvariable=apellido)
formularioDNI = ttk.Entry(formulario, textvariable=dni)
formularioHabitacion = ttk.Entry(formulario, textvariable=habitacion)
formularioFechaIngreso = DateEntry(
    formulario, selectmode="dia", textvariable=fechaIngreso)
formularioFechaSalida = DateEntry(
    formulario, selectmode="dia", textvariable=fechaSalida)

# botones
botonAccion = ttk.Button(formulario, textvariable=botonVariable, padding=(
    "10 5 10 5"), command=accionBoton)
botonCrear = ttk.Button(herramientas, text="Crear", padding=("10 5 10 5"),command=lambda: botonVariable.set("Guardar"))
botonActualizar = ttk.Button(
    herramientas, text="Actualizar", padding=("10 5 10 5"),command=lambda: botonVariable.set("Actualizar"))
botonEliminar = ttk.Button(
    herramientas, text="Eliminar", padding=("10 5 10 5"),command=borrarCliente)

# etiquetas
etiquetaNombre = ttk.Label(formulario, text="Nombre")
etiquetaApellido = ttk.Label(formulario, text="Apellido")
etiquetaDNI = ttk.Label(formulario, text="DNI")
etiquetaHabitacion = ttk.Label(formulario, text="Habitacion")
etiquetaFechaIngreso = ttk.Label(formulario, text="Fecha de Ingreso")
etiquetaFechaSalida = ttk.Label(formulario, text="Fechas de salida")

# se empaquetan los elementos
marco.grid(column=0, row=0, sticky=(N, S, E, W))
formulario.grid(column=0, row=0)
listaDatos.grid(column=0, row=1, pady=5)
herramientas.grid(column=0, row=2)

etiquetaNombre.grid(column=0, row=0, sticky=SW, padx=5)
formularioNombre.grid(column=0, row=1, sticky=(W), padx=5)

etiquetaApellido.grid(column=1, row=0, sticky=W, padx=5)
formularioApellido.grid(column=1, row=1, sticky=(W), padx=5)

etiquetaDNI.grid(column=2, row=0, sticky=W, padx=5)
formularioDNI.grid(column=2, row=1, sticky=(W), padx=5)

etiquetaHabitacion.grid(column=3, row=0, sticky=W, padx=5)
formularioHabitacion.grid(column=3, row=1, sticky=(W), padx=5)

etiquetaFechaIngreso.grid(column=4, row=0, sticky=W, padx=5)
formularioFechaIngreso.grid(column=4, row=1, sticky=(W), padx=5)

etiquetaFechaSalida.grid(column=5, row=0, sticky=W, padx=5)
formularioFechaSalida.grid(column=5, row=1, sticky=(W), padx=5)

botonAccion.grid(column=5, row=2, sticky=W, pady=10)
botonCrear.grid(column=0, row=0, sticky=W, padx=20)
botonActualizar.grid(column=1, row=0, sticky=W, padx=20)
botonEliminar.grid(column=2, row=0, sticky=W, padx=20)

# Lista de clientes
arbol = ttk.Treeview(listaDatos, columns=5)
leerCliente()
arbol['columns'] = ('nombre', 'apellido',
                    'habitacion', 'fecha ingreso', 'fecha salida')

arbol.grid(column=0, row=0)
arbol.column('#0', width=100, minwidth=10)
arbol.heading('#0', text='DNI')

arbol.column('nombre', width=120, minwidth=10)
arbol.heading('nombre', text='Nombre')

arbol.column('apellido', width=120, minwidth=10)
arbol.heading('apellido', text='Apellido')

arbol.column('habitacion', width=100, minwidth=10)
arbol.heading('habitacion', text='Habitacion')

arbol.column('fecha ingreso', width=100, minwidth=10)
arbol.heading('fecha ingreso', text='Fecha ingreso')

arbol.column('fecha salida', width=100, minwidth=10)
arbol.heading('fecha salida', text='Fecha Salida')

root.mainloop()
