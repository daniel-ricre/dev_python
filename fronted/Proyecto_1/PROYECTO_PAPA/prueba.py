import streamlit as st
import pandas as pd
import os

# 1. La parte BONITA de la interfaz (Esto NO lo hace Pandas)
st.title("📝 Registro de Nombres Mágico")
nombre = st.text_input("Escribe un nombre (ej: Pedro)")

# 2. La parte de ALMACENAR (Esto SÍ lo hace Pandas)
if st.button("Guardar Nombre"):
    if nombre:
        # Crear un mini DataFrame de 1 fila
        nuevo_dato = pd.DataFrame({"Nombres": [nombre]})

        # Lógica para añadirlo al archivo histórico
        archivo = 'lista_nombres.csv'
        if os.path.exists(archivo):
            df_existente = pd.read_csv(archivo)
            df_final = pd.concat([df_existente, nuevo_dato], ignore_index=True)
        else:
            df_final = nuevo_dato

        # Guardar el archivo (Magia de Pandas)
        df_final.to_csv(archivo, index=False)
        st.success(f"¡'{nombre}' guardado correctamente!")
        st.balloons()  # Efecto visual bonito

# 3. Mostrar la tabla bonita actualizada (Magia de Pandas)
if os.path.exists('lista_nombres.csv'):
    df_vista = pd.read_csv('lista_nombres.csv')
    st.dataframe(df_vista, use_container_width=True)
