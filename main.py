import streamlit as st
import pandas as pd

def load_data():
    # Cargar datos desde un CSV previamente generado (extraído del PDF)
    df = pd.read_csv("lista_precios_completa.csv")
    return df

def main():
    # Configuración de la página sin barra lateral
    st.set_page_config(page_title="Lista de Precios", layout="wide", initial_sidebar_state="collapsed")
    st.title("Lista de Precios")
    
    # Cargar datos
    df = load_data()
    
    # Obtener parámetros de la URL para la selección de línea
    default_lines = st.query_params.get("linea", [])
    
    # Buscador (filtra por Descripción o Clave)
    search_term = st.text_input("Buscar producto por descripción o clave", "")
    
    # Filtro de línea con valores por defecto provenientes de la URL
    all_lines = sorted(df["Línea"].unique().tolist())
    selected_lines = st.multiselect("Selecciona línea(s) de producto (opcional)", options=all_lines, default=default_lines)
    
    # Actualizar la URL con el filtro de línea seleccionado
    st.query_params.update(linea=selected_lines)
    
    # Selección del tipo de precio (único) con "Cj" como opción por defecto
    # price_options = ["Pub", "MM", "Cj", "min"]
    # selected_price = st.selectbox("Selecciona el tipo de precio a mostrar", options=price_options, index=price_options.index("Cj"))
    
    # Aplicar filtros al DataFrame
    df_filtered = df.copy()
    if search_term:
        df_filtered = df_filtered[
            df_filtered["Descripción"].str.contains(search_term, case=False, na=False) |
            df_filtered["Clave"].astype(str).str.contains(search_term, case=False, na=False)
        ]
    if selected_lines:
        df_filtered = df_filtered[df_filtered["Línea"].isin(selected_lines)]
    
    # Seleccionar las columnas a mostrar: Clave, Descripción y la columna del precio seleccionado
    df_to_display = df_filtered[["Clave", "Descripción", "Cj"]].copy()
    # Renombrar la columna del precio seleccionado a "Precio"
    df_to_display.rename(columns={"Cj": "Precio"}, inplace=True)
    
    # Mostrar la tabla sin índices
    st.markdown("### Resultados")
    if df_to_display.empty:
        st.info("No se encontraron productos con los filtros aplicados.")
    else:
        st.markdown(df_to_display.to_html(index=False), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
