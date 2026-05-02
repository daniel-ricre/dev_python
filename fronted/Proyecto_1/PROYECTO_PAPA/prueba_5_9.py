import PySimpleGUI as sg
import pandas as pd
import os
from datetime import datetime
import calendar
from openpyxl import load_workbook, Workbook
from openpyxl.styles import Font, PatternFill, Alignment

# --- Tema y constantes de diseño (sin cambios) ---
sg.theme('DarkBlack1')
sg.set_options(font=('Segoe UI', 10), dpi_awareness=True)

COLORS = {
    'bg': '#0A0A0A',
    'surface': '#18181B',
    'border': '#27272A',
    'text': '#FAFAFA',
    'text_secondary': '#A1A1AA',
    'accent': '#3B82F6',
    'success': '#10B981',
    'warning': '#F59E0B',
    'danger': '#EF4444'
}

CATEGORIAS = {
    'Vino': {'nombre': 'Vino', 'medida': 'Botellas', 'icono': '🍷', 'color': '#E11D48'},
    'Latas': {'nombre': 'Lata', 'medida': 'Unidades', 'icono': '🥫', 'color': '#2563EB'},
    'Dulces': {'nombre': 'Dulce', 'medida': 'Piezas', 'icono': '🍬', 'color': '#059669'}
}

ARCHIVO_EXCEL = 'inventario_db.xlsx'
HOJAS_EXCEL = {'Vino': 'VINO', 'Latas': 'LATAS', 'Dulces': 'DULCES'}

# --- Funciones Excel (optimizadas) ---


def init_excel():
    if not os.path.exists(ARCHIVO_EXCEL):
        with pd.ExcelWriter(ARCHIVO_EXCEL, engine='openpyxl') as writer:
            for cat in HOJAS_EXCEL.values():
                pd.DataFrame(columns=['Producto', 'Cantidad', 'Fecha', 'Hora']).to_excel(
                    writer, sheet_name=cat, index=False)
        wb = load_workbook(ARCHIVO_EXCEL)
        for cat, hoja in HOJAS_EXCEL.items():
            ws = wb[hoja]
            ws.column_dimensions['A'].width = 35
            ws.column_dimensions['B'].width = 12
            ws.column_dimensions['C'].width = 15
            ws.column_dimensions['D'].width = 12
            for cell in ws[1]:
                cell.font = Font(bold=True, color='FFFFFF')
                cell.fill = PatternFill(
                    start_color='27272A', end_color='27272A', fill_type='solid')
                cell.alignment = Alignment(horizontal='center')
        wb.save(ARCHIVO_EXCEL)


def guardar_registro(categoria, nombre, cantidad):
    try:
        fecha = datetime.now().strftime("%Y-%m-%d")
        hora = datetime.now().strftime("%H:%M")
        df_nuevo = pd.DataFrame([[nombre, cantidad, fecha, hora]], columns=[
                                'Producto', 'Cantidad', 'Fecha', 'Hora'])
        with pd.ExcelWriter(ARCHIVO_EXCEL, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
            writer.workbook = load_workbook(ARCHIVO_EXCEL)
            df_nuevo.to_excel(writer, sheet_name=HOJAS_EXCEL[categoria], index=False,
                              header=False, startrow=writer.sheets[HOJAS_EXCEL[categoria]].max_row)
        return True, "Guardado correctamente"
    except Exception as e:
        return False, str(e)


def obtener_registros(categoria, fecha_filtro=None):
    if not os.path.exists(ARCHIVO_EXCEL):
        return []
    try:
        df = pd.read_excel(ARCHIVO_EXCEL, sheet_name=HOJAS_EXCEL[categoria])
        if df.empty:
            return []
        if fecha_filtro:
            df = df[df['Fecha'] == fecha_filtro]
        return df.sort_values(by=['Fecha', 'Hora'], ascending=[False, False]).values.tolist()
    except Exception:
        return []


# --- Inicialización ---
init_excel()
fecha_actual = datetime.now()
fecha_seleccionada = fecha_actual
categoria_activa = 'Vino'

# --- Componentes UI (modulares) ---


def create_calendar_sidebar(year, month, selected_date):
    cal = calendar.monthcalendar(year, month)
    layout = [
        [sg.Text(f"{calendar.month_name[month].upper()} {year}", font=(
            'Segoe UI', 13, 'bold'), text_color=COLORS['text'])],
        [sg.Text("L  M  X  J  V  S  D", font=('Segoe UI', 8),
                 text_color=COLORS['text_secondary'], pad=(5, 5))],
    ]
    for week in cal:
        row = []
        for day in week:
            if day == 0:
                row.append(sg.Text('  ', size=(2, 1)))
            else:
                date_btn = datetime(year, month, day)
                if date_btn.date() == selected_date.date():
                    bg, txt = CATEGORIAS[categoria_activa]['color'], '#FFFFFF'
                elif date_btn.date() == datetime.now().date():
                    bg, txt = '#27272A', '#FACC15'
                else:
                    bg, txt = '#18181B', COLORS['text_secondary']
                btn = sg.Button(str(day), size=(2, 1), key=f'-CAL-{day}',
                                button_color=(txt, bg), border_width=0, font=('Segoe UI', 9, 'bold'), pad=(1, 2))
                row.append(btn)
        layout.append(row)
    layout.append([sg.Button('◀', size=(2, 1), key='-MES_ANT-', border_width=0, pad=(0, 5)),
                   sg.Button('▶', size=(2, 1),
                             key='-MES_SIG-', border_width=0),
                   sg.Push(),
                   sg.Button('HOY', size=(5, 1), key='-HOY-', border_width=0, button_color=(COLORS['text'], '#27272A'))])
    return layout


def create_category_sidebar():
    btns = []
    for cat_key, cat_val in CATEGORIAS.items():
        is_active = (cat_key == categoria_activa)
        btn_bg = cat_val['color'] if is_active else '#18181B'
        btn_txt = '#FFFFFF' if is_active else COLORS['text_secondary']
        # --- CORREGIDO: clave sin guión final ---
        btns.append([sg.Button(f"{cat_val['icono']}  {cat_key.upper()}", size=(15, 2), key=f'-CAT-{cat_key.upper()}',
                               button_color=(btn_txt, btn_bg), border_width=0, font=('Segoe UI', 11, 'bold'))])
    return btns


# --- Layout sin cambios en la estética ---
sidebar_col = sg.Column([
    [sg.Text('MENÚ', font=('Segoe UI', 10, 'bold'),
             text_color=COLORS['text_secondary'])],
    *create_category_sidebar(),
    [sg.Text('_' * 20, text_color=COLORS['border'])],
    [sg.Text('CALENDARIO', font=('Segoe UI', 10, 'bold'),
             text_color=COLORS['text_secondary'], pad=(0, 15))],
    [sg.Column(create_calendar_sidebar(fecha_actual.year,
               fecha_actual.month, fecha_seleccionada), key='-CAL_COL-')]
], background_color=COLORS['surface'], pad=(15, 15), vertical_alignment='top', element_justification='center')

data_col = sg.Column([
    [sg.Text(f'📋 INVENTARIO DE {categoria_activa.upper()}', font=(
        'Segoe UI', 14, 'bold'), text_color=COLORS['text'], key='-TITLE-')],
    [sg.Text(f'Vista del: {fecha_seleccionada.strftime("%d/%m/%Y")}', font=(
        'Segoe UI', 10), text_color=COLORS['text_secondary'], key='-SUBTITLE-')],
    [sg.Table(values=obtener_registros(categoria_activa, fecha_seleccionada.strftime("%Y-%m-%d")),
              headings=['Producto', 'Cant', 'Fecha', 'Hora'],
              col_widths=[35, 10, 15, 10],
              auto_size_columns=False,
              num_rows=20,
              key='-TABLE-',
              row_height=30,
              font=('Segoe UI', 10),
              header_font=('Segoe UI', 9, 'bold'),
              header_text_color='#A1A1AA',
              header_background_color='#18181B',
              alternating_row_color='#18181B',
              selected_row_colors=(
                  '#FFFFFF', CATEGORIAS[categoria_activa]['color']),
              expand_x=True, expand_y=True)],
    [sg.Button('🔄 Actualizar', size=(12, 1), button_color=(COLORS['text'], '#27272A'), border_width=0),
     sg.Button('📂 Abrir Excel', size=(12, 1), button_color=(
         COLORS['text'], '#27272A'), border_width=0),
     sg.Push(),
     sg.Button('📊 Ver Todos', size=(12, 1), button_color=(COLORS['text'], '#27272A'), border_width=0, key='-VER_TODOS-')]
], background_color=COLORS['bg'], pad=(20, 20), expand_x=True, expand_y=True)

form_col = sg.Column([
    [sg.Text('AÑADIR PRODUCTO', font=('Segoe UI', 13, 'bold'),
             text_color=COLORS['text'])],
    [sg.Text(f'Categoría activa: {categoria_activa}', font=(
        'Segoe UI', 10), text_color=CATEGORIAS[categoria_activa]['color'], key='-CAT_LABEL-')],
    [sg.HorizontalSeparator(color=COLORS['border'])],
    [sg.Text(f"Nombre del {CATEGORIAS[categoria_activa]['nombre']}",
             text_color=COLORS['text_secondary'])],
    [sg.Input(key='-NOMBRE-', size=(25, 1), background_color='#18181B',
              text_color=COLORS['text'], border_width=0)],
    [sg.Text(f"Cantidad ({CATEGORIAS[categoria_activa]['medida']})",
             text_color=COLORS['text_secondary'])],
    [sg.Input(key='-CANTIDAD-', size=(25, 1), background_color='#18181B',
              text_color=COLORS['text'], border_width=0)],
    [sg.Text('Fecha', text_color=COLORS['text_secondary'])],
    [sg.Input(key='-FECHA-', default_text=fecha_seleccionada.strftime("%Y-%m-%d"),
              size=(25, 1), background_color='#18181B', text_color=COLORS['text'], border_width=0)],
    [sg.Text('')],
    [sg.Button('💾  GUARDAR', size=(20, 2), key='-GUARDAR-',
               button_color=('#FFFFFF', CATEGORIAS[categoria_activa]['color']), border_width=0, font=('Segoe UI', 11, 'bold'))],
    [sg.Text('', key='-MSG-', size=(30, 2),
             text_color=COLORS['success'], font=('Segoe UI', 9))]
], background_color=COLORS['surface'], pad=(20, 20), vertical_alignment='top', element_justification='center')

layout = [[sidebar_col, sg.VSeparator(
    color=COLORS['border']), data_col, sg.VSeparator(color=COLORS['border']), form_col]]

window = sg.Window('Inventory Flow', layout, size=(1400, 750), margins=(0, 0),
                   background_color=COLORS['bg'], resizable=True, finalize=True)

# --- Función de refresco (CORREGIDA) ---


def refresh_ui_components():
    # 1. Actualizar botones de categoría (sin guion final)
    for cat in ['VINO', 'LATAS', 'DULCES']:
        is_active = (cat == categoria_activa.upper())
        # Mapeamos al diccionario original
        color_key = 'Vino' if cat == 'VINO' else (
            'Latas' if cat == 'LATAS' else 'Dulces')
        btn_bg = CATEGORIAS[color_key]['color'] if is_active else '#18181B'
        btn_txt = '#FFFFFF' if is_active else COLORS['text_secondary']
        # Clave corregida: sin guion final
        window[f'-CAT-{cat}'].update(button_color=(btn_txt, btn_bg))

    # 2. Títulos y colores contextuales
    window['-TITLE-'].update(f'📋 INVENTARIO DE {categoria_activa.upper()}')
    window['-CAT_LABEL-'].update(f'Categoría activa: {categoria_activa}',
                                 text_color=CATEGORIAS[categoria_activa]['color'])
    window['-GUARDAR-'].update(button_color=('#FFFFFF',
                               CATEGORIAS[categoria_activa]['color']))

    # 3. Refrescar calendario (reconstrucción controlada)
    window['-CAL_COL-'].Widget.children.clear()
    cal_layout = create_calendar_sidebar(
        fecha_actual.year, fecha_actual.month, fecha_seleccionada)
    for row in cal_layout:
        window.extend_layout(window['-CAL_COL-'], [row])

    # 4. Datos de tabla
    refresh_table_data()


def refresh_table_data(filtrar=True):
    fecha_str = fecha_seleccionada.strftime("%Y-%m-%d") if filtrar else None
    datos = obtener_registros(categoria_activa, fecha_str)
    window['-TABLE-'].update(values=datos)
    window['-TABLE-'].update(selected_row_colors=('#FFFFFF',
                             CATEGORIAS[categoria_activa]['color']))
    subtitle = f'Vista del: {fecha_seleccionada.strftime("%d/%m/%Y")}' if filtrar else 'Vista: TODOS LOS REGISTROS'
    window['-SUBTITLE-'].update(subtitle)


# Carga inicial
refresh_ui_components()

# --- Bucle de eventos (CORREGIDO) ---
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break

    # --- Cambio de categoría (claves corregidas) ---
    if event == '-CAT-VINO':
        categoria_activa = 'Vino'
        refresh_ui_components()
    elif event == '-CAT-LATAS':
        categoria_activa = 'Latas'
        refresh_ui_components()
    elif event == '-CAT-DULCES':
        categoria_activa = 'Dulces'
        refresh_ui_components()

    # --- Calendario ---
    if event.startswith('-CAL-'):
        dia = int(event.replace('-CAL-', ''))
        fecha_seleccionada = datetime(
            fecha_actual.year, fecha_actual.month, dia)
        window['-FECHA-'].update(fecha_seleccionada.strftime("%Y-%m-%d"))
        refresh_ui_components()

    if event == '-HOY-':
        fecha_seleccionada = datetime.now()
        fecha_actual = fecha_seleccionada
        window['-FECHA-'].update(fecha_seleccionada.strftime("%Y-%m-%d"))
        refresh_ui_components()

    if event == '-MES_ANT-':
        month = fecha_actual.month - 1
        year = fecha_actual.year
        if month < 1:
            month = 12
            year -= 1
        fecha_actual = datetime(year, month, 1)
        refresh_ui_components()

    if event == '-MES_SIG-':
        month = fecha_actual.month + 1
        year = fecha_actual.year
        if month > 12:
            month = 1
            year += 1
        fecha_actual = datetime(year, month, 1)
        refresh_ui_components()

    # --- Guardar producto ---
    if event == '-GUARDAR-':
        nombre = values['-NOMBRE-'].strip()
        cantidad = values['-CANTIDAD-'].strip()
        if not nombre or not cantidad:
            window['-MSG-'].update('❌ Campos vacíos',
                                   text_color=COLORS['danger'])
        elif not cantidad.isdigit():
            window['-MSG-'].update('❌ Cantidad inválida',
                                   text_color=COLORS['danger'])
        else:
            exito, msg = guardar_registro(
                categoria_activa, nombre, int(cantidad))
            if exito:
                window['-MSG-'].update(f'✅ {nombre} añadido',
                                       text_color=COLORS['success'])
                window['-NOMBRE-'].update('')
                window['-CANTIDAD-'].update('')
                refresh_table_data()
                window['-NOMBRE-'].set_focus()
            else:
                window['-MSG-'].update(f'❌ {msg}', text_color=COLORS['danger'])

    # --- Ver Todos / Actualizar ---
    if event == '-VER_TODOS-':
        refresh_table_data(filtrar=False)
    if event == '🔄 Actualizar':
        refresh_table_data()
        window['-MSG-'].update('✅ Vista actualizada',
                               text_color=COLORS['success'])

    # --- Abrir Excel ---
    if event == '📂 Abrir Excel':
        if os.path.exists(ARCHIVO_EXCEL):
            os.startfile(ARCHIVO_EXCEL)

window.close()
