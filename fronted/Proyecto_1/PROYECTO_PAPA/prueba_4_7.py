import PySimpleGUI as sg
import pandas as pd
import os
from datetime import datetime
import calendar
from openpyxl import load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

# --- Configuración de la ventana ---
sg.theme('LightBlue3')

# --- ÚNICO archivo Excel ---
ARCHIVO_EXCEL = 'registro_inventario.xlsx'
NOMBRE_HOJA = 'INVENTARIO'

# --- Configuración de etiquetas dinámicas por categoría ---
ETIQUETAS_CATEGORIA = {
    'Vino': {
        'nombre': 'Nombre del vino:',
        'cantidad': 'Cantidad (botellas):',
        'titulo': '🍷 VINO',
        'color_titulo': '8B0000',  # Rojo oscuro
        'color_encabezado': 'CD5C5C'  # Rojo indio
    },
    'Latas': {
        'nombre': 'Nombre de la lata:',
        'cantidad': 'Cantidad (unidades):',
        'titulo': '🥫 LATAS',
        'color_titulo': '00008B',  # Azul oscuro
        'color_encabezado': '4682B4'  # Azul acero
    },
    'Dulces': {
        'nombre': 'Nombre del dulce:',
        'cantidad': 'Cantidad (piezas):',
        'titulo': '🍬 DULCES',
        'color_titulo': '006400',  # Verde oscuro
        'color_encabezado': '3CB371'  # Verde mar
    }
}

# --- Función para inicializar el archivo Excel con las tres tablas ---


def inicializar_excel():
    """Crea el archivo Excel con las tres tablas en una sola hoja"""
    if not os.path.exists(ARCHIVO_EXCEL):
        # Crear un libro nuevo
        from openpyxl import Workbook
        wb = Workbook()
        ws = wb.active
        ws.title = NOMBRE_HOJA

        fila_actual = 1

        for categoria, etiquetas in ETIQUETAS_CATEGORIA.items():
            # Título de la tabla
            ws.merge_cells(f'A{fila_actual}:C{fila_actual}')
            celda_titulo = ws[f'A{fila_actual}']
            celda_titulo.value = etiquetas['titulo']
            celda_titulo.font = Font(size=14, bold=True, color='FFFFFF')
            celda_titulo.fill = PatternFill(start_color=etiquetas['color_titulo'],
                                            end_color=etiquetas['color_titulo'],
                                            fill_type='solid')
            celda_titulo.alignment = Alignment(
                horizontal='center', vertical='center')
            ws.row_dimensions[fila_actual].height = 30  # Título más alto

            fila_actual += 1

            # Encabezados de la tabla
            encabezados = ['Nombre', 'Cantidad', 'Fecha Registro']
            for col, encabezado in enumerate(encabezados, start=1):
                celda = ws.cell(row=fila_actual, column=col)
                celda.value = encabezado
                celda.font = Font(bold=True, color='FFFFFF', size=11)
                celda.fill = PatternFill(start_color=etiquetas['color_encabezado'],
                                         end_color=etiquetas['color_encabezado'],
                                         fill_type='solid')
                celda.alignment = Alignment(
                    horizontal='center', vertical='center')
                celda.border = Border(
                    left=Side(style='thin', color='000000'),
                    right=Side(style='thin', color='000000'),
                    top=Side(style='thin', color='000000'),
                    bottom=Side(style='thin', color='000000')
                )

            ws.row_dimensions[fila_actual].height = 25
            fila_actual += 1

            # Agregar una fila vacía con borde inferior para separar
            fila_actual += 1

            # Línea divisoria gruesa entre tablas
            if categoria != 'Dulces':  # No agregar después de la última tabla
                ws.merge_cells(f'A{fila_actual}:C{fila_actual}')
                celda_divisoria = ws[f'A{fila_actual}']
                celda_divisoria.border = Border(
                    bottom=Side(style='thick', color='000000')
                )
                ws.row_dimensions[fila_actual].height = 5
                fila_actual += 1

            # Espacio adicional entre tablas (5 filas vacías en total)
            for _ in range(4):  # 4 filas vacías adicionales
                fila_actual += 1

        # Ajustar ancho de columnas
        ws.column_dimensions['A'].width = 35
        ws.column_dimensions['B'].width = 15
        ws.column_dimensions['C'].width = 28

        wb.save(ARCHIVO_EXCEL)
        return True
    return False

# --- Función para guardar en la tabla correspondiente ---


def guardar_en_excel(categoria, nombre, cantidad, fecha_registro=None):
    """Añade un registro a la tabla específica dentro de la misma hoja"""
    if fecha_registro is None:
        fecha_registro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        # Asegurar que el archivo existe
        inicializar_excel()

        # Cargar el libro existente
        wb = load_workbook(ARCHIVO_EXCEL)
        ws = wb[NOMBRE_HOJA]

        # Encontrar la posición de la tabla de la categoría
        fila_tabla = encontrar_fila_tabla(
            ws, ETIQUETAS_CATEGORIA[categoria]['titulo'])

        if fila_tabla is None:
            return False, f"❌ No se encontró la tabla de {categoria}"

        # La tabla empieza 2 filas después del título (título + encabezados)
        fila_datos = fila_tabla + 2

        # Encontrar la primera fila vacía en esa tabla
        while ws.cell(row=fila_datos, column=1).value is not None:
            fila_datos += 1

        # Insertar el nuevo registro
        ws.cell(row=fila_datos, column=1, value=nombre)
        ws.cell(row=fila_datos, column=2, value=cantidad)
        ws.cell(row=fila_datos, column=3, value=fecha_registro)

        # Aplicar estilo a las celdas
        for col in range(1, 4):
            celda = ws.cell(row=fila_datos, column=col)
            celda.alignment = Alignment(
                horizontal='left', vertical='center', wrap_text=True)
            celda.border = Border(
                left=Side(style='thin', color='000000'),
                right=Side(style='thin', color='000000'),
                top=Side(style='thin', color='000000'),
                bottom=Side(style='thin', color='000000')
            )

        # Alternar colores de fondo para mejor legibilidad
        if (fila_datos - (fila_tabla + 2)) % 2 == 0:
            for col in range(1, 4):
                ws.cell(row=fila_datos, column=col).fill = PatternFill(
                    start_color='F5F5F5', end_color='F5F5F5', fill_type='solid'
                )

        wb.save(ARCHIVO_EXCEL)
        return True, f"✅ Registro guardado en {categoria}"

    except Exception as e:
        return False, f"❌ Error al guardar: {str(e)}"

# --- Función para encontrar la fila donde empieza una tabla ---


def encontrar_fila_tabla(ws, titulo_buscado):
    """Encuentra la fila donde está el título de una tabla específica"""
    for row in range(1, ws.max_row + 1):
        celda = ws.cell(row=row, column=1)
        if celda.value == titulo_buscado:
            return row
    return None

# --- Función para filtrar registros por fecha y categoría ---


def filtrar_por_fecha(categoria, fecha_objetivo):
    """Obtiene los registros de una tabla específica filtrados por fecha"""
    if not os.path.exists(ARCHIVO_EXCEL):
        return []

    try:
        wb = load_workbook(ARCHIVO_EXCEL, read_only=True)
        ws = wb[NOMBRE_HOJA]

        # Encontrar la tabla
        fila_tabla = encontrar_fila_tabla(
            ws, ETIQUETAS_CATEGORIA[categoria]['titulo'])

        if fila_tabla is None:
            wb.close()
            return []

        # Los datos empiezan 2 filas después del título
        fila_datos = fila_tabla + 2

        registros = []
        fecha_inicio = fecha_objetivo.replace(hour=0, minute=0, second=0)
        fecha_fin = fecha_objetivo.replace(hour=23, minute=59, second=59)

        # Leer fila por fila hasta encontrar una vacía
        while True:
            nombre = ws.cell(row=fila_datos, column=1).value
            if nombre is None:
                break

            cantidad = ws.cell(row=fila_datos, column=2).value
            fecha_str = ws.cell(row=fila_datos, column=3).value

            if fecha_str:
                try:
                    fecha_reg = pd.to_datetime(fecha_str)
                    if fecha_inicio <= fecha_reg <= fecha_fin:
                        registros.append([nombre, cantidad, fecha_str])
                except:
                    pass

            fila_datos += 1

        wb.close()

        # Ordenar por fecha (más reciente primero)
        registros.sort(key=lambda x: x[2], reverse=True)
        return registros

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
    [sg.Text('💡 Tip: El archivo Excel muestra TRES TABLAS separadas con colores distintos para cada categoría',
             text_color='gray', font=('Arial', 9), expand_x=True)]
]

# --- Crear ventana principal ---
window = sg.Window('Tienda Registro - 3 Tablas Separadas en Excel',
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
    if not os.path.exists(ARCHIVO_EXCEL):
        return False

    try:
        wb = load_workbook(ARCHIVO_EXCEL, read_only=True)
        ws = wb[NOMBRE_HOJA]

        fila_tabla = encontrar_fila_tabla(
            ws, ETIQUETAS_CATEGORIA[categoria]['titulo'])

        if fila_tabla is None:
            wb.close()
            return False

        fila_datos = fila_tabla + 2
        registros = []

        while True:
            nombre = ws.cell(row=fila_datos, column=1).value
            if nombre is None:
                break

            cantidad = ws.cell(row=fila_datos, column=2).value
            fecha = ws.cell(row=fila_datos, column=3).value
            registros.append([nombre, cantidad, fecha])
            fila_datos += 1

        wb.close()

        if registros:
            registros.sort(key=lambda x: x[2], reverse=True)
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
