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
    
    # Buscador en la parte superior (filtra por Descripción o Clave)
    search_term = st.text_input("Buscar producto por descripción o clave", "")
    
    # Filtros opcionales: selección múltiple para línea de producto y tipos de precio
    all_lines = sorted(df["Línea"].unique().tolist())
    selected_lines = st.multiselect("Selecciona línea(s) de producto (opcional)", options=all_lines)
    
    price_options = ["Pub", "MM", "Cj", "min"]
    selected_prices = st.multiselect("Selecciona tipo(s) de precio a mostrar (opcional)", options=price_options)
    if not selected_prices:
        selected_prices = price_options  # Mostrar todos si no se selecciona ninguno
    
    # Aplicar filtros al DataFrame
    df_filtered = df.copy()
    if search_term:
        df_filtered = df_filtered[
            df_filtered["Descripción"].str.contains(search_term, case=False, na=False) |
            df_filtered["Clave"].astype(str).str.contains(search_term, case=False, na=False)
        ]
    if selected_lines:
        df_filtered = df_filtered[df_filtered["Línea"].isin(selected_lines)]
    
    # Seleccionar las columnas a mostrar: Clave, Descripción y los tipos de precio seleccionados
    columns_to_show = ["Clave", "Descripción"] + selected_prices
    df_to_display = df_filtered[columns_to_show]
    
    # Mostrar la tabla resultante sin índices
    st.markdown("### Resultados")
    if df_to_display.empty:
        st.info("No se encontraron productos con los filtros aplicados.")
    else:
        st.markdown(df_to_display.to_html(index=False), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
