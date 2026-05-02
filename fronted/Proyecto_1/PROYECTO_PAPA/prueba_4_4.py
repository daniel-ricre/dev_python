import PySimpleGUI as sg
import pandas as pd
import os
from datetime import datetime
import calendar

# --- Configuración de la ventana ---
sg.theme('LightBlue3')

# --- ÚNICO archivo Excel con tres hojas ---
ARCHIVO_EXCEL = 'registro_inventario.xlsx'
HOJAS_EXCEL = {
    'Vino': 'VINO',
    'Latas': 'LATAS',
    'Dulces': 'DULCES'
}

# --- Configuración de etiquetas dinámicas por categoría ---
ETIQUETAS_CATEGORIA = {
    'Vino': {
        'nombre': 'Nombre del vino:',
        'cantidad': 'Cantidad (botellas):'
    },
    'Latas': {
        'nombre': 'Nombre de la lata:',
        'cantidad': 'Cantidad (unidades):'
    },
    'Dulces': {
        'nombre': 'Nombre del dulce:',
        'cantidad': 'Cantidad (piezas):'
    }
}

# --- Función para inicializar el archivo Excel con las tres hojas si no existe ---


def inicializar_excel():
    if not os.path.exists(ARCHIVO_EXCEL):
        with pd.ExcelWriter(ARCHIVO_EXCEL, engine='openpyxl') as writer:
            for categoria, hoja in HOJAS_EXCEL.items():
                df_vacio = pd.DataFrame(
                    columns=['Nombre', 'Cantidad', 'Fecha Registro'])
                df_vacio.to_excel(writer, sheet_name=hoja, index=False)

# --- Función para guardar en la hoja correspondiente ---


def guardar_en_excel(categoria, nombre, cantidad, fecha_registro=None):
    if fecha_registro is None:
        fecha_registro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    hoja = HOJAS_EXCEL[categoria]

    nuevo_registro = pd.DataFrame({
        'Nombre': [nombre],
        'Cantidad': [cantidad],
        'Fecha Registro': [fecha_registro]
    })

    try:
        # Asegurar que el archivo existe
        inicializar_excel()

        # Leer la hoja específica
        df_existente = pd.read_excel(ARCHIVO_EXCEL, sheet_name=hoja)

        # Concatenar el nuevo registro
        df_final = pd.concat([df_existente, nuevo_registro], ignore_index=True)

        # Guardar manteniendo las otras hojas
        with pd.ExcelWriter(ARCHIVO_EXCEL, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            df_final.to_excel(writer, sheet_name=hoja, index=False)

        return True, f"✅ Registro guardado en {categoria}"
    except Exception as e:
        return False, f"❌ Error: {str(e)}"

# --- Función para filtrar registros por fecha y categoría ---


def filtrar_por_fecha(categoria, fecha_objetivo):
    hoja = HOJAS_EXCEL[categoria]

    if not os.path.exists(ARCHIVO_EXCEL):
        return []

    try:
        df = pd.read_excel(ARCHIVO_EXCEL, sheet_name=hoja)
        if df.empty:
            return []

        df['Fecha Registro'] = pd.to_datetime(df['Fecha Registro'])

        fecha_inicio = fecha_objetivo.replace(hour=0, minute=0, second=0)
        fecha_fin = fecha_objetivo.replace(hour=23, minute=59, second=59)

        mascara = (df['Fecha Registro'] >= fecha_inicio) & (
            df['Fecha Registro'] <= fecha_fin)
        df_filtrado = df[mascara]

        # Ordenar por fecha (más reciente primero)
        df_filtrado = df_filtrado.sort_values(
            'Fecha Registro', ascending=False)

        return df_filtrado.values.tolist()
    except Exception as e:
        print(f"Error filtrando: {e}")
        return []

# --- Función para crear ventana de calendario ---


def mostrar_calendario(fecha_actual):
    año_actual = fecha_actual.year
    mes_actual = fecha_actual.month

    cal = calendar.monthcalendar(año_actual, mes_actual)

    layout_calendario = [
        [sg.Text(f"{calendar.month_name[mes_actual]} {año_actual}",
                 font=('Arial', 16, 'bold'),
                 justification='center',
                 expand_x=True)],
        [sg.Text('')],

        [sg.Text(dia, size=(4, 1), justification='center', font=('Arial', 10, 'bold'))
         for dia in ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom']],
    ]

    for semana in cal:
        fila_botones = []
        for dia in semana:
            if dia == 0:
                fila_botones.append(sg.Text('', size=(4, 2)))
            else:
                if (dia == fecha_actual.day and mes_actual == datetime.now().month
                        and año_actual == datetime.now().year):
                    color_boton = ('white', 'green')
                else:
                    color_boton = ('black', 'white')

                fila_botones.append(
                    sg.Button(str(dia),
                              size=(4, 2),
                              key=f'-DIA_CAL_{dia}-',
                              button_color=color_boton)
                )
        layout_calendario.append(fila_botones)

    layout_calendario.extend([
        [sg.Text('')],
        [sg.Button('◀ Mes Anterior', size=(12, 1), key='-MES_ANTERIOR-'),
         sg.Button('Hoy', size=(8, 1), key='-HOY-'),
         sg.Button('Mes Siguiente ▶', size=(12, 1), key='-MES_SIGUIENTE-')],
        [sg.Text('')],
        [sg.Button('Cancelar', size=(10, 1)),
         sg.Button('Seleccionar', size=(10, 1), button_color=('white', 'blue'))]
    ])

    window_cal = sg.Window('Seleccionar Fecha',
                           layout_calendario,
                           modal=True,
                           element_justification='center')

    fecha_seleccionada = None
    mes_temporal = mes_actual
    año_temporal = año_actual

    while True:
        event_cal, values_cal = window_cal.read()

        if event_cal in (sg.WINDOW_CLOSED, 'Cancelar'):
            break

        if event_cal == 'Seleccionar':
            if fecha_seleccionada:
                break
            else:
                sg.popup('Por favor selecciona un día primero', title='Aviso')

        if event_cal == '-HOY-':
            fecha_seleccionada = datetime.now()
            break

        if event_cal == '-MES_ANTERIOR-':
            mes_temporal -= 1
            if mes_temporal < 1:
                mes_temporal = 12
                año_temporal -= 1
            window_cal.close()
            fecha_temporal = datetime(año_temporal, mes_temporal, 1)
            fecha_seleccionada = mostrar_calendario(fecha_temporal)
            break

        if event_cal == '-MES_SIGUIENTE-':
            mes_temporal += 1
            if mes_temporal > 12:
                mes_temporal = 1
                año_temporal += 1
            window_cal.close()
            fecha_temporal = datetime(año_temporal, mes_temporal, 1)
            fecha_seleccionada = mostrar_calendario(fecha_temporal)
            break

        if event_cal.startswith('-DIA_CAL_'):
            dia = int(event_cal.replace('-DIA_CAL_', '').replace('-', ''))
            fecha_seleccionada = datetime(año_temporal, mes_temporal, dia)

    window_cal.close()
    return fecha_seleccionada


# --- Inicializar Excel al iniciar el programa ---
inicializar_excel()

# --- Obtener fecha actual ---
fecha_actual = datetime.now()
fecha_texto = fecha_actual.strftime("%d de %B de %Y")

# --- Variable global para categoría actual ---
categoria_actual = 'Vino'

# --- Diseño de la interfaz ---
layout = [
    # === SELECTOR DE CATEGORÍA ===
    [sg.Text('📦 SELECCIONAR CATEGORÍA', font=('Arial', 14, 'bold'),
             justification='center', expand_x=True)],

    [sg.Button('🍷 VINO', size=(15, 2), font=('Arial', 12, 'bold'),
               button_color=('white', 'darkred'), key='-CAT_VINO-'),
     sg.Button('🥫 LATAS', size=(15, 2), font=('Arial', 12, 'bold'),
               button_color=('white', 'darkblue'), key='-CAT_LATAS-'),
     sg.Button('🍬 DULCES', size=(15, 2), font=('Arial', 12, 'bold'),
               button_color=('white', 'darkgreen'), key='-CAT_DULCES-')],

    [sg.HorizontalSeparator()],

    # === SELECTOR DE FECHA ===
    [sg.Text('📅 FILTRAR POR FECHA', font=('Arial', 12, 'bold'),
             justification='center', expand_x=True)],

    [sg.Button('📆 Seleccionar Fecha', size=(20, 2), font=('Arial', 11, 'bold'),
               button_color=('white', 'purple'), key='-SELECCIONAR_FECHA-'),
     sg.Text(fecha_texto, key='-FECHA_MOSTRADA-', font=('Arial', 14, 'bold'),
             size=(30, 1), justification='center')],

    [sg.HorizontalSeparator()],
    [sg.Text('')],

    # === CONTENIDO PRINCIPAL ===
    [
        # COLUMNA IZQUIERDA: Tabla de registros
        sg.Column([
            [sg.Text('📋 REGISTROS DEL DÍA', font=('Arial', 12, 'bold'),
                     key='-TITULO_TABLA-')],
            [sg.Table(
                values=[],
                headings=['Nombre', 'Cantidad', 'Fecha Registro'],
                max_col_width=30,
                auto_size_columns=False,
                col_widths=[30, 15, 25],
                display_row_numbers=True,
                justification='left',
                num_rows=20,
                key='-TABLA-',
                row_height=25,
                enable_events=True,
                expand_x=True,
                expand_y=True
            )],
            [sg.Button('🔄 Actualizar', size=(15, 1)),
             sg.Button('📂 Abrir Excel', size=(15, 1),
                       button_color=('white', 'green')),
             sg.Button('📊 Ver Todos', size=(15, 1), button_color=('white', 'orange'))]
        ], expand_x=True, expand_y=True, scrollable=True),

        # COLUMNA DERECHA: Formulario con etiquetas dinámicas
        sg.Column([
            [sg.Text(f'✨ NUEVO REGISTRO - {categoria_actual.upper()}',
                     font=('Arial', 12, 'bold'), key='-TITULO_FORMULARIO-')],
            [sg.Text('')],

            [sg.Text(ETIQUETAS_CATEGORIA[categoria_actual]['nombre'],
                     size=(20, 1), key='-LABEL_NOMBRE-', font=('Arial', 11))],
            [sg.InputText(key='-NOMBRE-', size=(30, 1), font=('Arial', 11))],

            [sg.Text('')],

            [sg.Text(ETIQUETAS_CATEGORIA[categoria_actual]['cantidad'],
                     size=(20, 1), key='-LABEL_CANTIDAD-', font=('Arial', 11))],
            [sg.InputText(key='-CANTIDAD-', size=(30, 1), font=('Arial', 11))],

            [sg.Text('')],

            [sg.Text('Fecha de registro:', size=(20, 1))],
            [sg.InputText(key='-FECHA_REGISTRO-', size=(30, 1),
                          default_text=fecha_actual.strftime("%Y-%m-%d %H:%M"),
                          font=('Arial', 10), disabled=True)],

            [sg.Text('')],
            [sg.Text('')],

            [sg.Button('💾 Guardar Registro', size=(20, 2),
                       button_color=('white', 'blue'),
                       font=('Arial', 11, 'bold'),
                       bind_return_key=True,
                       key='-GUARDAR-')],

            [sg.Text('')],

            [sg.Text('', key='-MENSAJE-', size=(40, 2), text_color='green',
                     font=('Arial', 10), justification='center')],

            [sg.Text('')],
            [sg.Button('🗑️ Limpiar campos', size=(20, 1),
                       button_color=('white', 'gray'))]
        ], element_justification='center', vertical_alignment='top')
    ],

    # === BARRA DE ESTADO ===
    [sg.HorizontalSeparator()],
    [sg.Text('💡 Tip: El archivo Excel contiene tres hojas: VINO, LATAS y DULCES',
             text_color='gray', font=('Arial', 9), expand_x=True)]
]

# --- Crear ventana principal ---
window = sg.Window('Tienda Registro - Sistema de Inventario (Excel Unificado)',
                   layout,
                   size=(1050, 650),
                   resizable=True,
                   finalize=True)

# --- Variables globales ---
fecha_seleccionada_global = fecha_actual

# --- Función para actualizar la tabla con registros filtrados ---


def actualizar_tabla_por_fecha(categoria, fecha_filtro):
    registros = filtrar_por_fecha(categoria, fecha_filtro)
    window['-TABLA-'].update(values=registros)

    # Actualizar título de la tabla
    fecha_formateada = fecha_filtro.strftime("%d/%m/%Y")
    window['-TITULO_TABLA-'].update(
        f'📋 {categoria.upper()} - Registros del {fecha_formateada}')

    return len(registros) > 0

# --- Función para ver todos los registros de una categoría ---


def ver_todos_registros(categoria):
    hoja = HOJAS_EXCEL[categoria]

    if not os.path.exists(ARCHIVO_EXCEL):
        return False

    try:
        df = pd.read_excel(ARCHIVO_EXCEL, sheet_name=hoja)
        if not df.empty:
            # Ordenar por fecha (más reciente primero)
            df = df.sort_values('Fecha Registro', ascending=False)
            registros = df.values.tolist()
            window['-TABLA-'].update(values=registros)
            window['-TITULO_TABLA-'].update(
                f'📋 {categoria.upper()} - TODOS LOS REGISTROS')
            return True
    except Exception as e:
        sg.popup_error(f"Error al cargar: {e}")
    return False

# --- Función para cambiar de categoría ---


def cambiar_categoria(nueva_categoria):
    global categoria_actual
    categoria_actual = nueva_categoria

    # Actualizar etiquetas del formulario
    window['-LABEL_NOMBRE-'].update(
        ETIQUETAS_CATEGORIA[categoria_actual]['nombre'])
    window['-LABEL_CANTIDAD-'].update(
        ETIQUETAS_CATEGORIA[categoria_actual]['cantidad'])

    # Actualizar título del formulario
    window['-TITULO_FORMULARIO-'].update(
        f'✨ NUEVO REGISTRO - {categoria_actual.upper()}')

    # Actualizar tabla con la nueva categoría
    actualizar_tabla_por_fecha(categoria_actual, fecha_seleccionada_global)

    # Mensaje de confirmación
    window['-MENSAJE-'].update(
        f'✅ Categoría cambiada a {categoria_actual}', text_color='green')


# --- Cargar registros iniciales ---
actualizar_tabla_por_fecha(categoria_actual, fecha_actual)

# --- Bucle principal ---
while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED:
        break

    # Actualizar fecha mostrada
    window['-FECHA_MOSTRADA-'].update(
        fecha_seleccionada_global.strftime("%d de %B de %Y"))
    window['-FECHA_REGISTRO-'].update(
        fecha_seleccionada_global.strftime("%Y-%m-%d %H:%M"))

    # Cambiar categoría
    if event == '-CAT_VINO-':
        cambiar_categoria('Vino')
    elif event == '-CAT_LATAS-':
        cambiar_categoria('Latas')
    elif event == '-CAT_DULCES-':
        cambiar_categoria('Dulces')

    # Seleccionar fecha del calendario
    if event == '-SELECCIONAR_FECHA-':
        fecha_elegida = mostrar_calendario(fecha_seleccionada_global)
        if fecha_elegida:
            fecha_seleccionada_global = fecha_elegida
            actualizar_tabla_por_fecha(
                categoria_actual, fecha_seleccionada_global)
            window['-MENSAJE-'].update(f"✅ Mostrando registros del {fecha_elegida.strftime('%d/%m/%Y')}",
                                       text_color='green')

    # Guardar registro
    if event == '-GUARDAR-':
        nombre = values['-NOMBRE-'].strip()
        cantidad = values['-CANTIDAD-'].strip()

        if not nombre or not cantidad:
            window['-MENSAJE-'].update(
                "❌ Todos los campos son obligatorios", text_color='red')
        elif not cantidad.isdigit():
            window['-MENSAJE-'].update("❌ La cantidad debe ser un número",
                                       text_color='red')
        else:
            fecha_registro = fecha_seleccionada_global.strftime(
                "%Y-%m-%d %H:%M:%S")
            exito, mensaje = guardar_en_excel(
                categoria_actual, nombre, int(cantidad), fecha_registro)

            if exito:
                window['-MENSAJE-'].update(mensaje, text_color='green')
                window['-NOMBRE-'].update('')
                window['-CANTIDAD-'].update('')
                actualizar_tabla_por_fecha(
                    categoria_actual, fecha_seleccionada_global)
                window['-NOMBRE-'].set_focus()
            else:
                window['-MENSAJE-'].update(mensaje, text_color='red')

    # Actualizar tabla
    if event == '🔄 Actualizar':
        actualizar_tabla_por_fecha(categoria_actual, fecha_seleccionada_global)
        window['-MENSAJE-'].update("✅ Tabla actualizada", text_color='green')

    # Ver todos los registros
    if event == '📊 Ver Todos':
        if ver_todos_registros(categoria_actual):
            window['-MENSAJE-'].update(f"✅ Mostrando todos los registros de {categoria_actual}",
                                       text_color='green')
        else:
            window['-MENSAJE-'].update(f"ℹ️ No hay registros en {categoria_actual}",
                                       text_color='orange')

    # Abrir Excel
    if event == '📂 Abrir Excel':
        if os.path.exists(ARCHIVO_EXCEL):
            os.startfile(ARCHIVO_EXCEL)
        else:
            sg.popup("📁 Aún no hay archivo Excel. Guarda tu primer registro.",
                     title="Información")

    # Limpiar campos
    if event == '🗑️ Limpiar campos':
        window['-NOMBRE-'].update('')
        window['-CANTIDAD-'].update('')
        window['-MENSAJE-'].update("🧹 Campos limpiados", text_color='blue')
        window['-NOMBRE-'].set_focus()

window.close()
