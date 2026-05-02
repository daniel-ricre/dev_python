import PySimpleGUI as sg
import pandas as pd
import os
from datetime import datetime, timedelta
import calendar

# --- Configuración de la ventana ---
sg.theme('LightBlue3')

# --- Nombre del archivo Excel ---
ARCHIVO_EXCEL = 'registro_clientes.xlsx'

# --- Función para guardar en Excel con fecha específica ---


def guardar_en_excel(nombre, edad, numero, fecha_registro=None):
    if fecha_registro is None:
        fecha_registro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    nuevo_registro = pd.DataFrame({
        'Nombre': [nombre],
        'Edad': [edad],
        'Número': [numero],
        'Fecha Registro': [fecha_registro]
    })

    try:
        if os.path.exists(ARCHIVO_EXCEL):
            df_existente = pd.read_excel(ARCHIVO_EXCEL)
            df_final = pd.concat(
                [df_existente, nuevo_registro], ignore_index=True)
        else:
            df_final = nuevo_registro

        df_final.to_excel(ARCHIVO_EXCEL, index=False)
        return True, "✅ Registro guardado exitosamente"
    except Exception as e:
        return False, f"❌ Error: {str(e)}"

# --- Función para filtrar registros por fecha ---


def filtrar_por_fecha(fecha_objetivo):
    if not os.path.exists(ARCHIVO_EXCEL):
        return []

    try:
        df = pd.read_excel(ARCHIVO_EXCEL)
        if df.empty:
            return []

        # Convertir columna de fecha a datetime
        df['Fecha Registro'] = pd.to_datetime(df['Fecha Registro'])

        # Filtrar por la fecha seleccionada
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

    # Crear layout del calendario
    cal = calendar.monthcalendar(año_actual, mes_actual)

    layout_calendario = [
        [sg.Text(f"{calendar.month_name[mes_actual]} {año_actual}",
                 font=('Arial', 16, 'bold'),
                 justification='center',
                 expand_x=True)],
        [sg.Text('')],

        # Días de la semana
        [sg.Text(dia, size=(4, 1), justification='center', font=('Arial', 10, 'bold'))
         for dia in ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom']],
    ]

    # Agregar días del mes como botones
    for semana in cal:
        fila_botones = []
        for dia in semana:
            if dia == 0:
                # Día vacío
                fila_botones.append(sg.Text('', size=(4, 2)))
            else:
                # Destacar el día actual
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

    # Botones de navegación
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
    headings=['Nombre', 'Edad', 'Número', 'Fecha Registro'],
    max_col_width=30,
    auto_size_columns=False,
    col_widths=[20, 8, 15, 25],
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

# --- Diseño de la interfaz ---
layout = [
    # === SELECTOR DE FECHA (Reemplaza los días superiores) ===
    [sg.Text('📅 FECHA ACTUAL', font=('Arial', 12, 'bold'),
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
            [sg.Text('📋 REGISTROS DEL DÍA SELECCIONADO',
                     font=('Arial', 12, 'bold'), key='-TITULO_TABLA-')],
            [tabla_elemento],
            [sg.Button('🔄 Actualizar', size=(12, 1)),
             sg.Button('📂 Abrir Excel', size=(12, 1),
                       button_color=('white', 'green')),
             sg.Button('📊 Ver Todos', size=(12, 1),
                       button_color=('white', 'orange')),
             sg.Button('📈 Estadísticas', size=(12, 1), button_color=('white', 'blue'))]
        ], expand_x=True, expand_y=True, scrollable=True, vertical_scroll_only=False),

        # COLUMNA DERECHA: Formulario
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

            [sg.Text('Fecha:', size=(8, 1)),
             sg.InputText(key='-FECHA_REGISTRO-', size=(25, 1),
                          default_text=fecha_actual.strftime("%Y-%m-%d %H:%M"),
                          font=('Arial', 10), disabled=True)],

            [sg.Text('')],

            [sg.Button('💾 Guardar Registro', size=(20, 2),
                       button_color=('white', 'blue'),
                       font=('Arial', 11, 'bold'),
                       bind_return_key=True)],

            [sg.Text('')],

            [sg.Text('', key='-MENSAJE-', size=(35, 2),
                     text_color='green', font=('Arial', 10))],

            [sg.Text('')],
            [sg.Text('📊 Resumen del día:', font=('Arial', 10, 'bold'))],
            [sg.Text('', key='-RESUMEN_DIA-', size=(35, 4), font=('Arial', 9))],

            [sg.Text('')],
            [sg.Button('🗑️ Limpiar campos', size=(20, 1),
                       button_color=('white', 'gray'))]
        ], element_justification='center', vertical_alignment='top')
    ],

    # === BARRA DE ESTADO ===
    [sg.HorizontalSeparator()],
    [sg.Text('💡 Tip: Selecciona una fecha en el calendario para ver/filtrar registros',
             text_color='gray', font=('Arial', 9), expand_x=True)]
]

# --- Crear ventana principal ---
window = sg.Window('Tienda Registro - Sistema de Gestión por Fechas',
                   layout,
                   size=(1100, 650),
                   resizable=True,
                   finalize=True)

# --- Variables globales ---
fecha_seleccionada_global = fecha_actual

# --- Función para actualizar la tabla con registros filtrados ---


def actualizar_tabla_por_fecha(fecha_filtro):
    registros = filtrar_por_fecha(fecha_filtro)
    window['-TABLA-'].update(values=registros)

    # Actualizar título
    fecha_formateada = fecha_filtro.strftime("%d/%m/%Y")
    window['-TITULO_TABLA-'].update(f'📋 REGISTROS DEL {fecha_formateada}')

    # Actualizar resumen del día
    total = len(registros)
    if total > 0 and registros:
        edades = [int(r[1]) for r in registros if str(r[1]).isdigit()]
        promedio = sum(edades) / len(edades) if edades else 0
        resumen = f"📈 Total registros: {total}\n"
        resumen += f"📊 Promedio edad: {promedio:.1f} años\n"
        resumen += f"👥 Clientes únicos: {len(set(r[0] for r in registros))}"
    else:
        resumen = f"📈 Total registros: 0\n📊 Sin datos para mostrar"

    window['-RESUMEN_DIA-'].update(resumen)
    return total > 0

# --- Función para ver todos los registros ---


def ver_todos_registros():
    if os.path.exists(ARCHIVO_EXCEL):
        try:
            df = pd.read_excel(ARCHIVO_EXCEL)
            if not df.empty:
                registros = df.values.tolist()
                window['-TABLA-'].update(values=registros)
                window['-TITULO_TABLA-'].update('📋 TODOS LOS REGISTROS')
                window['-RESUMEN_DIA-'].update(
                    f"📈 Total histórico: {len(df)} registros")
                return True
        except Exception as e:
            sg.popup_error(f"Error al cargar: {e}")
    return False


# --- Cargar registros del día actual al iniciar ---
actualizar_tabla_por_fecha(fecha_actual)

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

    # Seleccionar fecha del calendario
    if event == '-SELECCIONAR_FECHA-':
        fecha_elegida = mostrar_calendario(fecha_seleccionada_global)
        if fecha_elegida:
            fecha_seleccionada_global = fecha_elegida
            actualizar_tabla_por_fecha(fecha_seleccionada_global)
            window['-MENSAJE-'].update(f"✅ Mostrando registros del {fecha_elegida.strftime('%d/%m/%Y')}",
                                       text_color='green')

    # Guardar registro con la fecha seleccionada
    if event == '💾 Guardar Registro':
        nombre = values['-NOMBRE-'].strip()
        edad = values['-EDAD-'].strip()
        numero = values['-NUMERO-'].strip()

        if not nombre or not edad or not numero:
            window['-MENSAJE-'].update(
                "❌ Todos los campos son obligatorios", text_color='red')
        elif not edad.isdigit():
            window['-MENSAJE-'].update("❌ La edad debe ser un número",
                                       text_color='red')
        else:
            fecha_registro = fecha_seleccionada_global.strftime(
                "%Y-%m-%d %H:%M:%S")
            exito, mensaje = guardar_en_excel(
                nombre, int(edad), numero, fecha_registro)

            if exito:
                window['-MENSAJE-'].update(mensaje, text_color='green')
                window['-NOMBRE-'].update('')
                window['-EDAD-'].update('')
                window['-NUMERO-'].update('')
                actualizar_tabla_por_fecha(fecha_seleccionada_global)
                window['-NOMBRE-'].set_focus()
            else:
                window['-MENSAJE-'].update(mensaje, text_color='red')

    # Actualizar tabla con fecha actual
    if event == '🔄 Actualizar':
        actualizar_tabla_por_fecha(fecha_seleccionada_global)
        window['-MENSAJE-'].update("✅ Tabla actualizada", text_color='green')

    # Ver todos los registros
    if event == '📊 Ver Todos':
        if ver_todos_registros():
            window['-MENSAJE-'].update(
                "✅ Mostrando todos los registros históricos", text_color='green')
        else:
            window['-MENSAJE-'].update("ℹ️ No hay registros aún",
                                       text_color='orange')

    # Estadísticas generales
    if event == '📈 Estadísticas':
        if os.path.exists(ARCHIVO_EXCEL):
            df = pd.read_excel(ARCHIVO_EXCEL)
            if not df.empty:
                stats = f"📊 ESTADÍSTICAS GENERALES\n\n"
                stats += f"• Total registros: {len(df)}\n"
                stats += f"• Clientes únicos: {df['Nombre'].nunique()}\n"
                stats += f"• Promedio edad: {df['Edad'].mean():.1f} años\n"
                stats += f"• Primera visita: {df['Fecha Registro'].min()}\n"
                stats += f"• Última visita: {df['Fecha Registro'].max()}"
                sg.popup(stats, title='Estadísticas Generales')

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
        window['-EDAD-'].update('')
        window['-NUMERO-'].update('')
        window['-MENSAJE-'].update("🧹 Campos limpiados", text_color='blue')
        window['-NOMBRE-'].set_focus()

window.close()
