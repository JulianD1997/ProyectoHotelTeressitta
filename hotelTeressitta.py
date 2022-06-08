import sqlite3
from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import datetime
import traceback

# Funciones
def conexion_SQL(consulta, parametros=()):
    mi_conexion = sqlite3.connect("HotelTeressitta")
    cursor = mi_conexion.cursor()
    try:
        cursor.execute(consulta, parametros)
        return cursor.fetchall()
    except Exception:
        traceback.print_exc()
    finally:
        mi_conexion.commit()

def crear_tabla():
    consulta = ('''--sql
        CREATE TABLE IF NOT EXISTS Clientes(
            ID  INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            nombre VARCHAR(75) NOT NULL,
            apellido VARCHAR(75) NOT NULL,
            DNI INTEGER(15) NOT NULL,
            habitacion INTEGER(6) NOT NULL,
            fechaDeIngreso DATE NOT NULL,
            fechaDESalida DATE NOT NULL
        );'''
                )
    conexion_SQL(consulta)

def validar_datos():
    return len(nombre.get()) != 0 and len(apellido.get()) != 0\
           and dni.get() != 0 and habitacion.get() != 0

def crear_cliente():
    if validar_datos():
        consulta = """--sql
            INSERT INTO Clientes
            values(NULL, ?, ?, ?, ?, ?, ?);
        """
        ingreso = datetime.strptime(fecha_ingreso.get(), '%d/%m/%y').date()
        salida = datetime.strptime(fecha_ingreso.get(), '%d/%m/%y').date()
        
        parametros = (nombre.get(), apellido.get(), dni.get(),
                      habitacion.get(), ingreso, salida)
        conexion_SQL(consulta, parametros)
        print("Cliente guardado correctamente")

    else:
        print("todos los datos son requeridos")

    leer_cliente()

def leer_cliente():
    # Se borrar los clientes del arbol
    clientes = arbol.get_children()
    for cliente in clientes:
        arbol.delete(cliente)
    
    consulta = ("""--sql
        SELECT * FROM Clientes ORDER BY apellido ASC;
    """)
    datos = conexion_SQL(consulta)
    for cliente in datos:
        arbol.insert("", "end", text=cliente[0],
                     values=(cliente[1], cliente[2],cliente[3], cliente[4],
                             cliente[5], cliente[6]))

def modificar_cliente():
    if validar_datos:
        consulta = """--sql
            UPDATE Clientes
            SET nombre = ?,
                apellido = ?, 
                DNI = ?,
                habitacion = ?,
                fechaDeIngreso = ?,
                fechaDeSalida = ?,
            where ID = ?;
        """
        ingreso = datetime.strptime(fecha_ingreso.get(), "%d/%m/%y").date()
        salida = datetime.strptime(fecha_ingreso.get(), "%d/%m/%y").date()
        parametros = (nombre.get(), apellido.get(), dni.get(),
                      habitacion.get(), ingreso, salida)
        conexion_SQL(consulta, parametros)
        leer_cliente()
    else:
        print("Todos los datos deben ser ingresados")

def borrar_cliente():
    consulta = """--sql
        DELETE FROM Clientes
        WHERE ID = ?;
    """
    ############
    parametros = ()
    conexion_SQL(consulta, parametros)
    leer_cliente()

def setear_forms():
    nombre.set("")
    apellido.set("")
    dni.set(0)
    habitacion.set(0)
    hoy = datetime.today().date()
    fecha = str(hoy.strftime('%d/%m/%y'))
    fecha_ingreso.set(fecha)
    fecha_salida.set(fecha)

def accion_boton():
    if boton_variable.get() == "Guardar":
        crear_cliente()
    else:
        modificar_cliente()

    boton_variable.set("Guardar")
    setear_forms()

root = Tk()
root.title("Hotel Teressitta")

# Variables
crear_tabla()
nombre = StringVar()
apellido = StringVar()
dni = IntVar()
habitacion = IntVar()
fecha_ingreso = StringVar()
fecha_salida = StringVar()
boton_variable = StringVar()
boton_variable.set("Guardar")

# Se declaran los Frames
marco = ttk.Frame(root, padding=10)
formulario = ttk.LabelFrame(
    marco, height=700, text="Formulario cliente", padding=10)
lista_datos = ttk.LabelFrame(
    marco, height=700, text="Lista de clientes", padding=10)
herramientas = ttk.LabelFrame(
    marco, height=700, text="Herramientas", padding=10)

# formularios
formulario_nombre = ttk.Entry(formulario, textvariable=nombre)
formulario_apellido = ttk.Entry(formulario, textvariable=apellido)
formulario_DNI = ttk.Entry(formulario, textvariable=dni)
formulario_habitacion = ttk.Entry(formulario, textvariable=habitacion)
formulario_fecha_ingreso = DateEntry(
    formulario, selectmode="dia", textvariable=fecha_ingreso)
formulario_fecha_salida = DateEntry(
    formulario, selectmode="dia", textvariable=fecha_salida)

# botones
boton_accion = ttk.Button(formulario, textvariable=boton_variable,
                         padding="10 5 10 5", command=accion_boton)
boton_crear = ttk.Button(herramientas, text="Crear", padding="10 5 10 5",
                        command=lambda: boton_variable.set("Guardar"))
boton_actualizar = ttk.Button(herramientas, text="Actualizar",
                             padding="10 5 10 5",
                             command=lambda: boton_variable.set("Actualizar"))
boton_eliminar = ttk.Button(herramientas, text="Eliminar",
                           padding="10 5 10 5", command=borrar_cliente)

# etiquetas
etiqueta_nombre = ttk.Label(formulario, text="Nombre")
etiqueta_apellido = ttk.Label(formulario, text="Apellido")
etiqueta_DNI = ttk.Label(formulario, text="DNI")
etiqueta_habitacion = ttk.Label(formulario, text="Habitacion")
etiqueta_fecha_ingreso = ttk.Label(formulario, text="Fecha de Ingreso")
etiqueta_fecha_salida = ttk.Label(formulario, text="Fechas de salida")

# se empaquetan los elementos
marco.grid(column=0, row=0)
formulario.grid(column=0, row=0)
lista_datos.grid(column=0, row=1, pady=5)
herramientas.grid(column=0, row=2)

etiqueta_nombre.grid(column=0, row=0, sticky=SW, padx=5)
formulario_nombre.grid(column=0, row=1, sticky=W, padx=5)
etiqueta_apellido.grid(column=1, row=0, sticky=W, padx=5)
formulario_apellido.grid(column=1, row=1, sticky=W, padx=5)
etiqueta_DNI.grid(column=2, row=0, sticky=W, padx=5)
formulario_DNI.grid(column=2, row=1, sticky=W, padx=5)
etiqueta_habitacion.grid(column=3, row=0, sticky=W, padx=5)
formulario_habitacion.grid(column=3, row=1, sticky=W, padx=5)
etiqueta_fecha_ingreso.grid(column=4, row=0, sticky=W, padx=5)
formulario_fecha_ingreso.grid(column=4, row=1, sticky=W, padx=5)
etiqueta_fecha_salida.grid(column=5, row=0, sticky=W, padx=5)
formulario_fecha_salida.grid(column=5, row=1, sticky=W, padx=5)

boton_accion.grid(column=5, row=2, sticky=W, pady=10)
boton_crear.grid(column=0, row=0, sticky=W, padx=20)
boton_actualizar.grid(column=1, row=0, sticky=W, padx=20)
boton_eliminar.grid(column=2, row=0, sticky=W, padx=20)

# Lista de clientes
arbol = ttk.Treeview(lista_datos)
leer_cliente()
arbol['columns'] = ('nombre', 'apellido','DNI', 'habitacion',
                    'fecha ingreso', 'fecha salida',)
arbol.grid(column=0, row=0)
arbol.column('#0', width=50, minwidth=10)
arbol.heading('#0', text='ID')
arbol.column('nombre', width=120, minwidth=10)
arbol.heading('nombre', text='Nombre')
arbol.column('apellido', width=120, minwidth=10)
arbol.heading('apellido', text='Apellido')
arbol.column('DNI', width=100, minwidth=10)
arbol.heading('DNI', text='DNI')
arbol.column('habitacion', width=100, minwidth=10)
arbol.heading('habitacion', text='Habitacion')
arbol.column('fecha ingreso', width=100, minwidth=10)
arbol.heading('fecha ingreso', text='Fecha ingreso')
arbol.column('fecha salida', width=100, minwidth=10)
arbol.heading('fecha salida', text='Fecha Salida')

root.mainloop()