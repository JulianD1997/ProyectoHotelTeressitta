import sqlite3
from tkinter import *
from tkinter import ttk
from pytest import Item
from tkcalendar import DateEntry
from datetime import datetime
from tkinter import messagebox
import traceback
import re

"""
    La Siguiente aplicacion busca optimizar la gestion de
    Clientes en un Hotel en el cual se introduce datos basicos
    del cliente, el numero de habitacion donde se va a hospedar
    el dia que ingreso y el dia de salida.
"""
global id_cliente
global habitaciones_hotel
habitaciones_hotel = [101, 102, 103, 104, 201, 202,
                      203, 204, 301, 302, 303, 304]


# Funciones
def conexion_sql(consulta, parametros=()):
    mi_conexion = sqlite3.connect("HotelTeressitta")
    cursor = mi_conexion.cursor()
    try:
        cursor.execute(consulta, parametros)
        return cursor.fetchall()
    except Exception:
        traceback.print_exc()
        return False
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
    conexion_sql(consulta)


def validar_datos():  # Validar que los formularios no esten vacios.
    error = ""

    if not re.match("^[ a-zA-ZÀ-ÿ\u00f1\u00d1]+$", nombre.get()):
        error = error\
                + "\n - Nombre: Solo letras y espacios. Debe rellenar."

    if not re.match("^[ a-zA-ZÀ-ÿ\u00f1\u00d1]+$", apellido.get()):
        error = error\
                + "\n - Apellido: Solo letras y espacios. Debe rellenar."

    if not re.match("^[0-9]{8}$", dni.get()):
        error = error\
                + "\n - DNI: Solo números sin puntos. Longitud 8."

    if not re.match("^[0-3]0[0-4]$", habitacion.get()):
        error = error\
                + "\n - Habitación: Debe seleccionar una opción de la lista."

    if error:
        error = "Campos Incorrectos:\n" + error

    return error


def crear_cliente():
    error_validacion = validar_datos()

    if not error_validacion:
        consulta = """--sql
            INSERT INTO Clientes
            values(NULL, ?, ?, ?, ?, ?, ?);
        """
        ingreso = datetime.strptime(fecha_ingreso.get(), '%Y-%m-%d').date()
        salida = datetime.strptime(fecha_ingreso.get(), '%Y-%m-%d').date()

        parametros = (nombre.get(), apellido.get(), dni.get(),
                      habitacion.get(), ingreso, salida)
        print(parametros)
        datos = conexion_sql(consulta, parametros)
        if datos is not False:
            messagebox.showinfo("Crear Cliente",
                                "EL cliente fue creado correctamente")
            setear_forms()
        else:
            messagebox.showinfo("Crear Cliente",
                                "Hubo un error, el cliente no fue guardado")
    else:
        messagebox.showinfo("Crear Cliente", error_validacion)
    leer_cliente()
    habitaciones_disponibles()


def leer_cliente():
    # Se borran todos los datos del arbol
    clientes = arbol.get_children()
    for cliente in clientes:
        arbol.delete(cliente)
    
    consulta = ("""--sql
        SELECT * FROM Clientes ORDER BY apellido ASC;
    """)
    datos = conexion_sql(consulta)
    for cliente in datos:
        arbol.insert("", "end", text=cliente[0],
                     values=(cliente[1], cliente[2], cliente[3], cliente[4],
                             cliente[5], cliente[6]))


def modificar_cliente():
    error_validacion = validar_datos()

    if not error_validacion:
        consulta = """--sql
            UPDATE Clientes
            SET nombre = ?,
                apellido = ?, 
                DNI = ?,
                habitacion = ?,
                fechaDeIngreso = ?,
                fechaDeSalida = ?
            WHERE ID = ?;
        """
        ingreso = datetime.strptime(fecha_ingreso.get(), '%Y-%m-%d').date()
        salida = datetime.strptime(fecha_salida.get(), '%Y-%m-%d').date()
        parametros = (nombre.get(), apellido.get(), dni.get(),
                      habitacion.get(), ingreso, salida, id_cliente)
        datos = conexion_sql(consulta, parametros)
        if datos is not False:
            messagebox.showinfo("Modificar Cliente",
                                "El cliente fue modificado correctamente")
            setear_forms()
        else:
            messagebox.showinfo("Crear Cliente",
                                "Hubo un error, el cliente no fue modificado")
    else:
        messagebox.showinfo("Modificar Cliente", error_validacion)
    leer_cliente()
    habitaciones_disponibles()


def borrar_cliente():
    global id_cliente
    cliente = arbol.item(arbol.focus())
    respuesta = messagebox.askyesno("Borrar cliente",
                                    "¿Desea borrar el cliente?")
    if respuesta:
        id_cliente = cliente['text']
        consulta = """--sql
            DELETE FROM Clientes
            WHERE ID = ?;
        """
        parametros = (id_cliente,)
        datos = conexion_sql(consulta, parametros)
        if datos is not False:
            messagebox.showinfo("Borrar Cliente",
                                "EL cliente fue borrado correctamente")
        else:
            messagebox.showinfo("Borrar Cliente",
                                "Hubo un error,EL cliente no fue borrado")
    leer_cliente()
    habitaciones_disponibles()


def setear_forms():  # Limpiar los formularios
    boton_variable.set("Guardar")
    nombre.set("")
    apellido.set("")
    dni.set("")
    habitacion.set("Seleccionar")
    hoy = datetime.now()
    fecha = str(hoy.strftime("%Y-%m-%d"))
    fecha_ingreso.set(fecha)
    fecha_salida.set(fecha)


def accion_boton():  # La accion que realizara el boton del formulario
    
    if boton_variable.get() == "Guardar":
        crear_cliente()
    else:
        modificar_cliente()


def mostrar_datos():  # Enviar los datos del cliente a modificar
    global id_cliente
    boton_variable.set("Actualizar")
    cliente = arbol.item(arbol.focus())
    id_cliente = cliente['text']
    nombre.set(cliente['values'][0])
    apellido.set(cliente['values'][1])
    dni.set(cliente['values'][2])
    habitacion.set((cliente['values'][3]))
    fecha_ingreso.set(str(cliente['values'][4]))
    fecha_salida.set(str(cliente['values'][5]))


def habitaciones_disponibles():  # ComboBox de habitaciones disponibles
    habitaciones_ocupadas = []
    consulta = """--sql
        SELECT habitacion 
        FROM Clientes 
        WHERE fechaDeSalida >= ?;
    """
    hoy = datetime.now()
    fecha = hoy.strftime("%Y-%m-%d")
    parametros = (fecha,)
    datos = conexion_sql(consulta, parametros)
    for habitacion in datos:
        habitaciones_ocupadas.append(habitacion[0])
    comboBox_Habitaciones["values"] = list(set(habitaciones_hotel)
                                           - set(habitaciones_ocupadas))
    return comboBox_Habitaciones


root = Tk()
root.title("Hotel Teressitta")
root.resizable(False, False)
crear_tabla()

# Variables

nombre = StringVar()
apellido = StringVar()
dni = StringVar()
habitacion = StringVar()
fecha_ingreso = StringVar()
fecha_salida = StringVar()
boton_variable = StringVar()
habitacion.set("Seleccionar")
boton_variable.set("Guardar")

# Se declaran los Frames
marco = ttk.Frame(root, padding=10)
formulario = ttk.LabelFrame(
    marco, height=700, text="Formulario cliente", padding=10)
lista_datos = ttk.LabelFrame(
    marco, height=700, text="Lista de clientes", padding=10)
herramientas = ttk.LabelFrame(
    marco, height=700, text="Herramientas", padding=10)

# ComboBox
comboBox_Habitaciones = ttk.Combobox(formulario, textvariable=habitacion)
habitaciones_disponibles()

# Formularios
formulario_nombre = ttk.Entry(formulario, textvariable=nombre)
formulario_apellido = ttk.Entry(formulario, textvariable=apellido)
formulario_DNI = ttk.Entry(formulario, textvariable=dni)
formulario_habitacion = ttk.Entry(formulario, textvariable=habitacion)
formulario_fecha_ingreso = DateEntry(formulario, selectmode="dia",
                                     date_pattern='yyyy-MM-dd',
                                     textvariable=fecha_ingreso)
formulario_fecha_salida = DateEntry(formulario, selectmode="dia",
                                    date_pattern='yyyy-MM-dd',
                                    textvariable=fecha_salida)

# Botones
boton_accion = ttk.Button(formulario, textvariable=boton_variable,
                          padding="10 5 10 5", command=accion_boton)
boton_crear = ttk.Button(herramientas, text="Crear", padding="10 5 10 5",
                         command=setear_forms)
boton_actualizar = ttk.Button(herramientas, text="Actualizar",
                              padding="10 5 10 5",
                              command=mostrar_datos)
boton_borrar = ttk.Button(herramientas, text="Borrar",
                          padding="10 5 10 5", command=borrar_cliente)

# Etiquetas
etiqueta_nombre = ttk.Label(formulario, text="Nombre")
etiqueta_apellido = ttk.Label(formulario, text="Apellido")
etiqueta_DNI = ttk.Label(formulario, text="DNI")
etiqueta_habitacion = ttk.Label(formulario, text="Habitacion")
etiqueta_fecha_ingreso = ttk.Label(formulario, text="Fecha de Ingreso")
etiqueta_fecha_salida = ttk.Label(formulario, text="Fechas de salida")

# Se empaquetan los elementos
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
comboBox_Habitaciones.grid(column=3, row=1, sticky=W, padx=5)
etiqueta_fecha_ingreso.grid(column=4, row=0, sticky=W, padx=5)
formulario_fecha_ingreso.grid(column=4, row=1, sticky=W, padx=5)
etiqueta_fecha_salida.grid(column=5, row=0, sticky=W, padx=5)
formulario_fecha_salida.grid(column=5, row=1, sticky=W, padx=5)

boton_accion.grid(column=5, row=2, sticky=W, pady=10)
boton_crear.grid(column=0, row=0, sticky=W, padx=20)
boton_actualizar.grid(column=1, row=0, sticky=W, padx=20)
boton_borrar.grid(column=2, row=0, sticky=W, padx=20)

# Lista de clientes
arbol = ttk.Treeview(lista_datos)
leer_cliente()
arbol['columns'] = ('nombre', 'apellido', 'DNI', 'habitacion',
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
