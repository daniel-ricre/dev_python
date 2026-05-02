import PySimpleGUI as sg
import pandas as pd
import os
from datetime import datetime
import calendar

# --- Configuración de la ventana ---
sg.theme('LightBlue3')

# --- Archivos Excel por categoría ---
ARCHIVOS_EXCEL = {
    'Vino': 'registro_vinos.xlsx',
    'Latas': 'registro_latas.xlsx',
    'Dulces': 'registro_dulces.xlsx'
}

# --- Configuración de campos por categoría ---
CAMPOS_CATEGORIA = {
    'Vino': [
        {'nombre': 'Nombre del Vino', 'key': '-NOMBRE-', 'tipo': 'texto'},
        {'nombre': 'Cantidad (botellas)',
         'key': '-CANTIDAD-', 'tipo': 'numero'}
    ],
    'Latas': [
        {'nombre': 'Nombre de la Lata', 'key': '-NOMBRE-', 'tipo': 'texto'},
        {'nombre': 'Cantidad (unidades)',
         'key': '-CANTIDAD-', 'tipo': 'numero'}
    ],
    'Dulces': [
        {'nombre': 'Nombre del Dulce', 'key': '-NOMBRE-', 'tipo': 'texto'},
        {'nombre': 'Cantidad (piezas)', 'key': '-CANTIDAD-', 'tipo': 'numero'}
    ]
}

# --- Función para guardar en Excel según categoría ---


def guardar_en_excel(categoria, nombre, cantidad, fecha_registro=None):
    if fecha_registro is None:
        fecha_registro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    archivo = ARCHIVOS_EXCEL[categoria]

    nuevo_registro = pd.DataFrame({
        'Nombre': [nombre],
        'Cantidad': [cantidad],
        'Fecha Registro': [fecha_registro]
    })

    try:
        if os.path.exists(archivo):
            df_existente = pd.read_excel(archivo)
            df_final = pd.concat(
                [df_existente, nuevo_registro], ignore_index=True)
        else:
            df_final = nuevo_registro

        df_final.to_excel(archivo, index=False)
        return True, f"✅ Registro guardado en {categoria}"
    except Exception as e:
        return False, f"❌ Error: {str(e)}"

# --- Función para filtrar registros por fecha y categoría ---


def filtrar_por_fecha(categoria, fecha_objetivo):
    archivo = ARCHIVOS_EXCEL[categoria]
    if not os.path.exists(archivo):
        return []

    try:
        df = pd.read_excel(archivo)
        if df.empty:
            return []

        df['Fecha Registro'] = pd.to_datetime(df['Fecha Registro'])

        fecha_inicio = fecha_objetivo.replace(hour=0, minute=0, second=0)
        fecha_fin = fecha_objetivo.replace(hour=23, minute=59, second=59)

        mascara = (df['Fecha Registro'] >= fecha_inicio) & (
            df['Fecha Registro'] <= fecha_fin)
        df_filtrado = df[mascara]

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


# --- Elemento de la tabla expandible ---
tabla_elemento = sg.Table(
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
)

# --- Obtener fecha actual ---
fecha_actual = datetime.now()
fecha_texto = fecha_actual.strftime("%d de %B de %Y")

# --- Variable global para categoría actual ---
categoria_actual = 'Vino'

# --- Función para crear los campos dinámicos según categoría ---


def crear_campos_categoria(categoria):
    campos = []
    for campo in CAMPOS_CATEGORIA[categoria]:
        campos.append([
            sg.Text(f'{campo["nombre"]}:', size=(18, 1)),
            sg.InputText(key=campo['key'], size=(25, 1), font=('Arial', 11))
        ])
    return campos


# --- Diseño de la interfaz ---
layout = [
    # === SELECTOR DE CATEGORÍA (Principal) ===
    [sg.Text('📦 CATEGORÍA DE PRODUCTOS', font=('Arial', 12, 'bold'),
             justification='center', expand_x=True)],

    [sg.Button('🍷 VINO', size=(15, 2), font=('Arial', 11, 'bold'),
               button_color=('white', 'darkred'), key='-CAT_VINO-'),
     sg.Button('🥫 LATAS', size=(15, 2), font=('Arial', 11, 'bold'),
               button_color=('white', 'darkblue'), key='-CAT_LATAS-'),
     sg.Button('🍬 DULCES', size=(15, 2), font=('Arial', 11, 'bold'),
               button_color=('white', 'darkgreen'), key='-CAT_DULCES-')],

    [sg.Text(f'📍 Categoría actual: {categoria_actual}',
             key='-CATEGORIA_ACTUAL-', font=('Arial', 11, 'italic'),
             text_color='purple', expand_x=True)],

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
            [tabla_elemento],
            [sg.Button('🔄 Actualizar', size=(12, 1)),
             sg.Button('📂 Abrir Excel', size=(12, 1),
                       button_color=('white', 'green')),
             sg.Button('📊 Ver Todos', size=(12, 1),
                       button_color=('white', 'orange')),
             sg.Button('📈 Resumen', size=(12, 1), button_color=('white', 'blue'))]
        ], expand_x=True, expand_y=True, scrollable=True, vertical_scroll_only=False),

        # COLUMNA DERECHA: Formulario dinámico
        sg.Column([
            [sg.Text('✨ NUEVO REGISTRO', font=('Arial', 12, 'bold'))],
            [sg.Text('')],

            # Campos dinámicos que cambiarán según categoría
            *crear_campos_categoria(categoria_actual),

            [sg.Text('')],

            [sg.Text('Fecha:', size=(8, 1)),
             sg.InputText(key='-FECHA_REGISTRO-', size=(25, 1),
                          default_text=fecha_actual.strftime("%Y-%m-%d %H:%M"),
                          font=('Arial', 10), disabled=True)],

            [sg.Text('')],

            [sg.Button('💾 Guardar Registro', size=(20, 2),
                       button_color=('white', 'blue'),
                       font=('Arial', 11, 'bold'),
                       bind_return_key=True,
                       key='-GUARDAR-')],

            [sg.Text('')],

            [sg.Text('', key='-MENSAJE-', size=(35, 2),
                     text_color='green', font=('Arial', 10))],

            [sg.Text('')],
            [sg.Text('📊 Resumen del día:', font=('Arial', 10, 'bold'))],
            [sg.Text('', key='-RESUMEN_DIA-', size=(35, 5), font=('Arial', 9))],

            [sg.Text('')],
            [sg.Button('🗑️ Limpiar campos', size=(20, 1),
                       button_color=('white', 'gray'))]
        ], element_justification='center', vertical_alignment='top', key='-COLUMNA_FORMULARIO-')
    ],

    # === BARRA DE ESTADO ===
    [sg.HorizontalSeparator()],
    [sg.Text('💡 Tip: Selecciona una categoría y fecha para gestionar tu inventario',
             text_color='gray', font=('Arial', 9), expand_x=True)]
]

# --- Crear ventana principal ---
window = sg.Window('Tienda Registro - Sistema de Inventario por Categorías',
                   layout,
                   size=(1100, 650),
                   resizable=True,
                   finalize=True)

# --- Variables globales ---
fecha_seleccionada_global = fecha_actual

# --- Función para actualizar la tabla con registros filtrados ---


def actualizar_tabla_por_fecha(categoria, fecha_filtro):
    registros = filtrar_por_fecha(categoria, fecha_filtro)
    window['-TABLA-'].update(values=registros)

    # Actualizar título
    fecha_formateada = fecha_filtro.strftime("%d/%m/%Y")
    window['-TITULO_TABLA-'].update(
        f'📋 {categoria.upper()} - Registros del {fecha_formateada}')

    # Actualizar resumen del día
    total = len(registros)
    if total > 0 and registros:
        cantidades = [int(r[1]) for r in registros if str(r[1]).isdigit()]
        total_cantidad = sum(cantidades)
        promedio = total_cantidad / total if total > 0 else 0

        resumen = f"📦 Total registros: {total}\n"
        resumen += f"🔢 Total unidades: {total_cantidad}\n"
        resumen += f"📊 Promedio por registro: {promedio:.1f}\n"
        resumen += f"📝 Productos únicos: {len(set(r[0] for r in registros))}"
    else:
        resumen = f"📦 Total registros: 0\n📊 Sin datos para mostrar"

    window['-RESUMEN_DIA-'].update(resumen)
    return total > 0

# --- Función para ver todos los registros de una categoría ---


def ver_todos_registros(categoria):
    archivo = ARCHIVOS_EXCEL[categoria]
    if os.path.exists(archivo):
        try:
            df = pd.read_excel(archivo)
            if not df.empty:
                registros = df.values.tolist()
                window['-TABLA-'].update(values=registros)
                window['-TITULO_TABLA-'].update(
                    f'📋 {categoria.upper()} - TODOS LOS REGISTROS')

                # Resumen histórico
                total_cantidad = df['Cantidad'].sum(
                ) if 'Cantidad' in df.columns else 0
                window['-RESUMEN_DIA-'].update(
                    f"📦 Total histórico: {len(df)} registros\n"
                    f"🔢 Total unidades: {total_cantidad}\n"
                    f"📝 Productos únicos: {df['Nombre'].nunique()}"
                )
                return True
        except Exception as e:
            sg.popup_error(f"Error al cargar: {e}")
    return False

# --- Función para cambiar de categoría ---


def cambiar_categoria(nueva_categoria):
    global categoria_actual
    categoria_actual = nueva_categoria

    # Actualizar texto de categoría actual
    window['-CATEGORIA_ACTUAL-'].update(
        f'📍 Categoría actual: {categoria_actual}')

    # Recrear los campos del formulario
    window['-COLUMNA_FORMULARIO-'].Widget.children.clear()

    # Crear nuevo layout para la columna
    nuevo_layout = [
        [sg.Text('✨ NUEVO REGISTRO', font=('Arial', 12, 'bold'))],
        [sg.Text('')],
    ]

    # Agregar campos según categoría
    for campo in CAMPOS_CATEGORIA[categoria_actual]:
        nuevo_layout.append([
            sg.Text(f'{campo["nombre"]}:', size=(18, 1)),
            sg.InputText(key=campo['key'], size=(25, 1), font=('Arial', 11))
        ])

    nuevo_layout.extend([
        [sg.Text('')],
        [sg.Text('Fecha:', size=(8, 1)),
         sg.InputText(key='-FECHA_REGISTRO-', size=(25, 1),
                      default_text=fecha_seleccionada_global.strftime(
                          "%Y-%m-%d %H:%M"),
                      font=('Arial', 10), disabled=True)],
        [sg.Text('')],
        [sg.Button('💾 Guardar Registro', size=(20, 2),
                   button_color=('white', 'blue'),
                   font=('Arial', 11, 'bold'),
                   bind_return_key=True,
                   key='-GUARDAR-')],
        [sg.Text('')],
        [sg.Text('', key='-MENSAJE-', size=(35, 2),
                 text_color='green', font=('Arial', 10))],
        [sg.Text('')],
        [sg.Text('📊 Resumen del día:', font=('Arial', 10, 'bold'))],
        [sg.Text('', key='-RESUMEN_DIA-', size=(35, 5), font=('Arial', 9))],
        [sg.Text('')],
        [sg.Button('🗑️ Limpiar campos', size=(20, 1),
                   button_color=('white', 'gray'))]
    ])

    # Reconstruir la columna
    for fila in nuevo_layout:
        window.extend_layout(window['-COLUMNA_FORMULARIO-'], [fila])

    # Actualizar tabla con la nueva categoría
    actualizar_tabla_por_fecha(categoria_actual, fecha_seleccionada_global)


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

    # Resumen general
    if event == '📈 Resumen':
        archivo = ARCHIVOS_EXCEL[categoria_actual]
        if os.path.exists(archivo):
            df = pd.read_excel(archivo)
            if not df.empty:
                # Producto más registrado
                producto_top = df['Nombre'].value_counts().head(1)

                resumen = f"📊 RESUMEN DE {categoria_actual.upper()}\n\n"
                resumen += f"• Total registros: {len(df)}\n"
                resumen += f"• Total unidades: {df['Cantidad'].sum()}\n"
                resumen += f"• Productos únicos: {df['Nombre'].nunique()}\n"
                if not producto_top.empty:
                    resumen += f"• Más popular: {producto_top.index[0]} ({producto_top.values[0]} veces)\n"
                resumen += f"• Promedio por registro: {df['Cantidad'].mean():.1f} unidades"

                sg.popup(resumen, title=f'Resumen de {categoria_actual}')

    # Abrir Excel de la categoría actual
    if event == '📂 Abrir Excel':
        archivo = ARCHIVOS_EXCEL[categoria_actual]
        if os.path.exists(archivo):
            os.startfile(archivo)
        else:
            sg.popup(f"📁 Aún no hay archivo Excel para {categoria_actual}. Guarda tu primer registro.",
                     title="Información")

    # Limpiar campos
    if event == '🗑️ Limpiar campos':
        window['-NOMBRE-'].update('')
        window['-CANTIDAD-'].update('')
        window['-MENSAJE-'].update("🧹 Campos limpiados", text_color='blue')
        window['-NOMBRE-'].set_focus()

window.close()
