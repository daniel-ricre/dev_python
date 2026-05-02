import PySimpleGUI as sg
import pandas as pd
import os
from datetime import datetime, timedelta

# --- Configuración de la ventana ---
sg.theme('LightBlue3')  # Tema limpio y profesional

# --- Nombre del archivo Excel ---
ARCHIVO_EXCEL = 'registro_clientes.xlsx'

# --- Función para generar las fechas de la semana actual ---


def obtener_fechas_semana():
    hoy = datetime.now()
    # Encontrar el lunes de esta semana
    lunes = hoy - timedelta(days=hoy.weekday())

    dias_semana = ['Lunes', 'Martes', 'Miércoles',
                   'Jueves', 'Viernes', 'Sábado', 'Domingo']
    fechas_formato = []

    for i, dia in enumerate(dias_semana):
        fecha = lunes + timedelta(days=i)
        fechas_formato.append(f"{dia} ({fecha.day})")

    return fechas_formato

# --- Función para guardar en Excel ---


def guardar_en_excel(nombre, edad, numero):
    # Crear DataFrame con los nuevos datos
    nuevo_registro = pd.DataFrame({
        'Nombre': [nombre],
        'Edad': [edad],
        'Número': [numero],
        'Fecha Registro': [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
    })

    try:
        if os.path.exists(ARCHIVO_EXCEL):
            # Si el archivo existe, leer y añadir
            df_existente = pd.read_excel(ARCHIVO_EXCEL)
            df_final = pd.concat(
                [df_existente, nuevo_registro], ignore_index=True)
        else:
            # Si no existe, crear nuevo
            df_final = nuevo_registro

        # Guardar en Excel
        df_final.to_excel(ARCHIVO_EXCEL, index=False)
        return True, "✅ Registro guardado exitosamente"
    except Exception as e:
        return False, f"❌ Error: {str(e)}"


# --- Obtener fechas para mostrar ---
fechas_semana = obtener_fechas_semana()

# --- Diseño de la interfaz ---
layout = [
    # === PARTE SUPERIOR: DÍAS DE LA SEMANA ===
    [sg.Text('📅 SEMANA ACTUAL', font=('Arial', 14, 'bold'),
             justification='center', expand_x=True)],
    [sg.HorizontalSeparator()],

    # Botones con los días (Lunes(23), Martes(24), etc.)
    [sg.Button(dia, size=(12, 2), font=('Arial', 10),
               key=f'-DIA_{i}-') for i, dia in enumerate(fechas_semana)],

    [sg.HorizontalSeparator()],
    [sg.Text('')],  # Espacio

    # === CONTENIDO PRINCIPAL (Dividido en dos columnas) ===
    [
        # COLUMNA IZQUIERDA: Tabla de registros existentes
        sg.Column([
            [sg.Text('📋 REGISTROS GUARDADOS', font=('Arial', 12, 'bold'))],
            [sg.Table(
                values=[],
                headings=['Nombre', 'Edad', 'Número', 'Fecha'],
                max_col_width=25,
                auto_size_columns=True,
                display_row_numbers=True,
                justification='left',
                num_rows=15,
                key='-TABLA-',
                row_height=25,
                enable_events=True
            )],
            [sg.Button('Actualizar Tabla', size=(15, 1)),
             sg.Button('Abrir Excel', size=(15, 1), button_color=('white', 'green'))]
        ], expand_x=True, expand_y=True),

        # COLUMNA DERECHA: Formulario de ingreso
        sg.Column([
            [sg.Text('✨ NUEVO REGISTRO', font=('Arial', 12, 'bold'))],
            [sg.Text('')],

            [sg.Text('Nombre:', size=(8, 1)),
             sg.InputText(key='-NOMBRE-', size=(25, 1), font=('Arial', 11))],

            [sg.Text('Edad:', size=(8, 1)),
             sg.InputText(key='-EDAD-', size=(25, 1), font=('Arial', 11))],

            [sg.Text('Número:', size=(8, 1)),
             sg.InputText(key='-NUMERO-', size=(25, 1), font=('Arial', 11))],

            [sg.Text('')],

            [sg.Button('💾 Guardar Registro', size=(20, 2),
                       button_color=('white', 'blue'),
                       font=('Arial', 11, 'bold'),
                       bind_return_key=True)],

            [sg.Text('')],

            [sg.Text('', key='-MENSAJE-', size=(30, 2),
                     text_color='green', font=('Arial', 10))],

            [sg.Text('')],
            [sg.Text('📊 Estadísticas rápidas:', font=('Arial', 10, 'bold'))],
            [sg.Text('', key='-ESTADISTICAS-', size=(30, 3), font=('Arial', 9))]
        ], element_justification='center', vertical_alignment='top')
    ]
]

# --- Crear ventana ---
window = sg.Window('Tienda Registro - Sistema de Gestión',
                   layout,
                   size=(1000, 600),
                   resizable=True,
                   finalize=True)

# --- Función para cargar datos en la tabla ---


def cargar_datos_tabla():
    if os.path.exists(ARCHIVO_EXCEL):
        try:
            df = pd.read_excel(ARCHIVO_EXCEL)
            if not df.empty:
                datos_tabla = df.values.tolist()
                window['-TABLA-'].update(values=datos_tabla)

                # Actualizar estadísticas
                total_registros = len(df)
                promedio_edad = df['Edad'].mean(
                ) if 'Edad' in df.columns else 0
                stats_text = f"Total registros: {total_registros}\n"
                stats_text += f"Promedio edad: {promedio_edad:.1f} años"
                window['-ESTADISTICAS-'].update(stats_text)
                return True
        except Exception as e:
            print(f"Error cargando datos: {e}")
            window['-MENSAJE-'].update(
                f"Error: Instala openpyxl con 'pip install openpyxl'", text_color='red')
    return False


# --- Cargar datos iniciales ---
cargar_datos_tabla()

# --- Bucle principal ---
while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED:
        break

    # Manejar clic en los días de la semana (CORREGIDO)
    if event.startswith('-DIA_'):
        try:
            # Extraer el índice del día (el número después de "DIA_")
            indice = int(event.split('_')[1].split('-')[0])
            dia_seleccionado = fechas_semana[indice]
            sg.popup(f"📌 Has seleccionado: {dia_seleccionado}",
                     title="Día Seleccionado")
        except (ValueError, IndexError):
            # Si hay algún error al parsear, simplemente mostramos el evento
            sg.popup(f"📌 Has seleccionado un día",
                     title="Día Seleccionado")

    # Guardar registro
    if event == '💾 Guardar Registro':
        nombre = values['-NOMBRE-'].strip()
        edad = values['-EDAD-'].strip()
        numero = values['-NUMERO-'].strip()

        # Validaciones
        if not nombre or not edad or not numero:
            window['-MENSAJE-'].update(
                "❌ Todos los campos son obligatorios", text_color='red')
        elif not edad.isdigit():
            window['-MENSAJE-'].update("❌ La edad debe ser un número",
                                       text_color='red')
        else:
            exito, mensaje = guardar_en_excel(nombre, int(edad), numero)

            if exito:
                window['-MENSAJE-'].update(mensaje, text_color='green')
                # Limpiar campos
                window['-NOMBRE-'].update('')
                window['-EDAD-'].update('')
                window['-NUMERO-'].update('')
                # Actualizar tabla
                cargar_datos_tabla()
                # Efecto visual
                window['-NOMBRE-'].set_focus()
            else:
                window['-MENSAJE-'].update(mensaje, text_color='red')

    # Actualizar tabla manualmente
    if event == 'Actualizar Tabla':
        if cargar_datos_tabla():
            window['-MENSAJE-'].update("✅ Tabla actualizada",
                                       text_color='green')
        else:
            window['-MENSAJE-'].update("ℹ️ No hay registros aún",
                                       text_color='orange')

    # Abrir archivo Excel
    if event == 'Abrir Excel':
        if os.path.exists(ARCHIVO_EXCEL):
            os.startfile(ARCHIVO_EXCEL)  # Windows
        else:
            sg.popup("Aún no hay archivo Excel. Guarda tu primer registro.",
                     title="Información")

window.close()
