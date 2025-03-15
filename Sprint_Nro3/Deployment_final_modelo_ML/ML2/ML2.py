import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from PIL import Image
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Construir la ruta al CSV dentro del proyecto
ruta_csv = os.path.join(BASE_DIR, "data_example", "sample_reviews_ML1.csv")

# Cargar el CSV con pandas
df = pd.read_csv(ruta_csv, encoding="utf-8", delimiter=",", quotechar='"', header=None, names=["rating", "text"])

# Configurar la interfaz de la aplicación
st.set_page_config(page_title="Top Restaurantes en California", layout="wide")

# Estado de sesión para controlar las vistas
if "pagina_actual" not in st.session_state:
    st.session_state.pagina_actual = "inicio"

def volver_inicio():
    st.session_state.pagina_actual = "inicio"

# Página de inicio (selección de ciudad)
if st.session_state.pagina_actual == "inicio":
    # Cargar imágenes

    # Obtener la ruta absoluta de la carpeta donde está ML1.py
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # Construir las rutas de las imágenes
    logo_app_path = os.path.join(BASE_DIR, "Imagenes", "logo.jpg")
    logo_client_path = os.path.join(BASE_DIR, "Imagenes", "invertur.png")

    # Cargar las imágenes con PIL
    logo_app = Image.open(logo_app_path)
    logo_client = Image.open(logo_client_path)

    # Usar columnas para alinear el título y los logos en una fila
    col1, col2, col3 = st.columns([1, 6, 1])
    with col1:
        st.image(logo_app, width=150, caption='Insigh Labs')  # Logo ampliado
    with col2:
        st.markdown("<h1 style='text-align: center;'>🌎 Mapa de Restaurantes en California</h1>", unsafe_allow_html=True)
    with col3:
        st.image(logo_client, width=150, caption='Invertur')  # Logo ampliado


    # Selección de ciudad
    ciudades_disponibles = sorted(df["city"].dropna().unique())  # Filtrar valores nulos
    ciudad_seleccionada = st.selectbox("Selecciona una ciudad:", ciudades_disponibles)

    # Botón de búsqueda
    if st.button("🔍 Buscar restaurantes"):
        st.session_state.pagina_actual = "resultados"
        st.session_state.ciudad_seleccionada = ciudad_seleccionada
        st.rerun()

# Página de resultados (tabla y mapa)
elif st.session_state.pagina_actual == "resultados":
    ciudad_seleccionada = st.session_state.ciudad_seleccionada

    st.subheader(f"🏆 Top Restaurantes en {ciudad_seleccionada}")

    # Filtrar datos de la ciudad seleccionada
    df_filtrado = df[df["city"] == ciudad_seleccionada].dropna(subset=["latitude", "longitude"])

    if df_filtrado.empty:
        st.warning("No hay datos disponibles para esta ciudad.")
    else:
        # Mostrar la tabla con los datos
        st.write(df_filtrado[["name", "address", "avg_rating", "num_of_reviews"]])

        # Calcular el centro promedio de los puntos para centrar el mapa
        latitud_media = df_filtrado["latitude"].mean()
        longitud_media = df_filtrado["longitude"].mean()

        # Crear el mapa centrado en la ciudad seleccionada
        mapa = folium.Map(location=[latitud_media, longitud_media], zoom_start=13)

        # Agregar marcadores de los restaurantes en el mapa
        for _, row in df_filtrado.iterrows():
            nombre = row["name"]
            direccion = row["address"]
            puntuacion = row["avg_rating"]
            num_resenas = row["num_of_reviews"]
            lat, lon = row["latitude"], row["longitude"]

            folium.Marker(
                location=[lat, lon],
                popup=f"{nombre}\n📍 {direccion}\n⭐ {puntuacion} ({num_resenas} reseñas)",
                icon=folium.Icon(color="blue", icon="info-sign"),
            ).add_to(mapa)

        # Mostrar el mapa debajo de la tabla
        folium_static(mapa)

    # Botón para volver a la página principal
    if st.button("↩ Volver a la página principal"):
        volver_inicio()
        st.rerun()
