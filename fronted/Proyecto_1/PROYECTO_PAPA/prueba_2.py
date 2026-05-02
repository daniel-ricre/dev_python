import PySimpleGUI as sg
import pandas as pd
import os

# --- Configuración de la ventana ---
sg.theme('SystemDefaultForReal')  # Le da un aspecto moderno y limpio

# --- Nombre del archivo donde se guardan los datos ---
ARCHIVO_DATOS = 'registro_nombres.csv'

# --- Diseño de la ventana (lo que se ve en pantalla) ---
layout = [
    [sg.Text('✨ REGISTRO DE CLIENTES', font=('Helvetica', 16),
             justification='center', expand_x=True)],
    [sg.Text('')],  # Espacio decorativo

    [sg.Text('Nombre:', size=(10, 1)),
     sg.InputText(key='-NOMBRE-', size=(30, 1), font=('Arial', 12))],

    [sg.Text('')],  # Espacio decorativo

    [sg.Button('Guardar Nombre', size=(15, 1), bind_return_key=True),
     sg.Button('Ver Registros', size=(15, 1)),
     sg.Button('Salir', size=(8, 1))],

    [sg.Text('')],  # Espacio decorativo

    # Área para mostrar mensajes de estado (éxito, error, etc.)
    [sg.Text('', key='-MENSAJE-', size=(50, 1), text_color='green')]
]

# --- Crear la ventana principal con el título deseado ---
window = sg.Window('Tienda Registro', layout,
                   element_justification='center', finalize=True)

# --- Función para guardar los datos con Pandas ---


def guardar_nombre(nombre):
    if not nombre:
        return False, "El nombre no puede estar vacío."

    # Crear un DataFrame con el nuevo dato
    nuevo_dato = pd.DataFrame({'Nombres': [nombre]})

    try:
        # Si el archivo ya existe, añadir sin repetir el encabezado
        if os.path.exists(ARCHIVO_DATOS):
            nuevo_dato.to_csv(ARCHIVO_DATOS, mode='a',
                              header=False, index=False)
        else:
            # Si no existe, crearlo con el encabezado
            nuevo_dato.to_csv(ARCHIVO_DATOS, mode='w',
                              header=True, index=False)
        return True, f"'{nombre}' guardado exitosamente."
    except Exception as e:
        return False, f"Error al guardar: {e}"

# --- Función para mostrar los registros en una ventana emergente ---


def mostrar_registros():
    if not os.path.exists(ARCHIVO_DATOS):
        sg.popup("📋 No hay registros aún", title="Registros")
        return

    try:
        df = pd.read_csv(ARCHIVO_DATOS)
        if df.empty:
            sg.popup("📋 No hay registros aún", title="Registros")
            return

        # Convertir los datos a una lista de listas para la tabla
        datos_tabla = df.values.tolist()
        encabezados = df.columns.tolist()

        # Crear una ventana con una tabla para mostrar los datos
        layout_tabla = [
            [sg.Table(values=datos_tabla, headings=encabezados,
                      max_col_width=25, auto_size_columns=True,
                      display_row_numbers=True, justification='left',
                      num_rows=min(15, len(datos_tabla)), key='-TABLA-',
                      row_height=25)],
            [sg.Button('Cerrar', size=(10, 1))]
        ]

        window_tabla = sg.Window(
            '📋 Registros Guardados', layout_tabla, modal=True)
        while True:
            event, _ = window_tabla.read()
            if event in (sg.WINDOW_CLOSED, 'Cerrar'):
                break
        window_tabla.close()

    except Exception as e:
        sg.popup_error(f"Error al leer los datos: {e}")


# --- Bucle principal: mantiene la ventana abierta y procesa los clics ---
while True:
    event, values = window.read()

    # Si el usuario cierra la ventana o presiona 'Salir'
    if event in (sg.WINDOW_CLOSED, 'Salir'):
        break

    # Si presiona 'Guardar Nombre' o Enter en el campo de texto
    if event == 'Guardar Nombre':
        nombre_ingresado = values['-NOMBRE-'].strip()
        exito, mensaje = guardar_nombre(nombre_ingresado)

        if exito:
            window['-MENSAJE-'].update(mensaje, text_color='green')
            # Limpiar el campo para un nuevo ingreso
            window['-NOMBRE-'].update('')
        else:
            window['-MENSAJE-'].update(mensaje, text_color='red')

    # Si presiona 'Ver Registros'
    if event == 'Ver Registros':
        mostrar_registros()

# Cerrar la ventana al salir del bucle
window.close()
