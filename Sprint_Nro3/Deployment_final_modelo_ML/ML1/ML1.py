import streamlit as st
from nltk.sentiment import SentimentIntensityAnalyzer
import spacy
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from PIL import Image
import pandas as pd

# Configurar la página
st.set_page_config(layout="wide", page_title="Análisis de Reseñas")

# Cargar imágenes
logo_app = Image.open("D:/Soy Henry/Proyecto Final/yelp-google-reviews/Imagenes/logo.jpg")
logo_client = Image.open("D:/Soy Henry/Proyecto Final/yelp-google-reviews/Imagenes/invertur.png")

# Cargar el CSV
ruta_csv=r"D:\Soy Henry\Proyecto Final\yelp-google-reviews\Sprint_Nro3\Deployment_final_modelo_ML\data_example\sample_reviews_ML1.csv"
df = pd.read_csv(ruta_csv, encoding="utf-8", delimiter=",", quotechar='"', header=None, names=["rating", "text"])




# Asegurar que la sesión tenga estado inicializado
if 'pagina_actual' not in st.session_state:
    st.session_state['pagina_actual'] = "principal"
if 'reseña' not in st.session_state:
    st.session_state['reseña'] = ""
if 'calificacion' not in st.session_state:
    st.session_state['calificacion'] = 0


# Usar columnas para alinear el título y los logos en una fila
col1, col2, col3 = st.columns([1, 6, 1])
with col1:
    st.image(logo_app, width=150, caption='Insigh Labs')  # Logo ampliado
with col2:
    st.markdown("<h1 style='text-align: center;'>Sentimientos y Entidades en Reseñas de Clientes</h1>", unsafe_allow_html=True)
with col3:
    st.image(logo_client, width=150, caption='Invertur')  # Logo ampliado


# Inicializar el analizador de sentimiento y cargar el modelo de spaCy
sia = SentimentIntensityAnalyzer()
nlp = spacy.load(r"D:\Soy Henry\Proyecto Final\yelp-google-reviews\Sprint_Nro3\Deployment_final_modelo_ML\adjusted_model")
nlp_fun = spacy.load("en_core_web_sm")

# Función para extraer adjetivos y adverbios con spaCy
def extraer_palabras_clave(reseña):
    doc = nlp_fun(reseña)
    adjetivos_adverbios = [token.text for token in doc if token.pos_ in ['ADJ', 'ADV']]
    return adjetivos_adverbios



# Función para la página principal
def pagina_principal():
    st.title("Reseñas de Restaurantes")

    # Mostrar reseñas en formato de lista
    for i, row in df.iterrows():
        if st.button(f"{row['text']} ⭐ {row['rating']}"):
            st.session_state['reseña'] = row['text']
            st.session_state['calificacion'] = int(float(row['rating']))  # Convertir a float y luego a int
            st.session_state['pagina_actual'] = "resultados"
            st.rerun()




# Función para la página de resultados
def pagina_resultados():
    # Mostrar la reseña y calificación guardadas
    if 'reseña' in st.session_state and 'calificacion' in st.session_state:
        reseña = st.session_state['reseña']
        calificacion = st.session_state['calificacion']

# Mostrar la reseña citada y centrada
        st.markdown(f"""
            <div style="text-align: center; font-size: 1.2em; font-style: italic;">
                <p>"{reseña}"</p>
            </div>
        """, unsafe_allow_html=True)

        # Mostrar las estrellas centradas debajo de la reseña
        estrellas = ("⭐" * calificacion)
        st.markdown(f"""
            <div style="text-align: center; font-size: 1.5em; color: gold;">
                <strong>{estrellas}</strong>
            </div>
        """, unsafe_allow_html=True)

    # Análisis de sentimiento
    sentimiento = sia.polarity_scores(reseña)
    compound = sentimiento["compound"]

    # Botón de análisis
    
    if st.button("🔍 Analizar Sentimiento"):
    # Obtener la calificación desde session_state si ya fue asignada
        calificacion = st.session_state.calificacion if "calificacion" in st.session_state else 0
    
    # Extraer adjetivos y adverbios
        palabras_clave = extraer_palabras_clave(reseña)

    # Obtener los valores originales de VADER
        pos = sentimiento['pos']
        neu = sentimiento['neu']
        neg = sentimiento['neg']

    # Ajustar el valor de "neutral" si la calificación es distinta de 3
        if calificacion != 3:
            neu /= 10  # Reducimos el peso del neutral dividiéndolo por 10
            eliminado = sentimiento['neu'] - neu  # Cuánto se redujo el neutral
            
            # Distribuirlo proporcionalmente según la relación pos/neg
            total_sentimiento = pos + neg
            if total_sentimiento > 0:  # Evitar división por cero
                pos += eliminado * (pos / total_sentimiento)
                neg += eliminado * (neg / total_sentimiento)

    # Distribuir la visualización en columnas
        col1, col2 = st.columns(2)

        with col1:
            # Mostrar la calificación en estrellas con el mismo estilo CSS
            if calificacion >= 4:
                st.markdown(f"""
                    <div style="border: 2px solid #4CAF50; padding: 10px; border-radius: 5px;">
                        <h4>⭐ Calificación:</h4>
                        <p style="font-size: 1.2em; color: #4CAF50;"><strong>Reseña positiva 😊 ({calificacion}⭐)</strong></p>
                    </div>
                """, unsafe_allow_html=True)
            elif calificacion == 3:
                st.markdown(f"""
                    <div style="border: 2px solid #FF9800; padding: 10px; border-radius: 5px;">
                        <h4>⭐ Calificación:</h4>
                        <p style="font-size: 1.2em; color: #FF9800;"><strong>Reseña neutral 😐 ({calificacion}⭐)</strong></p>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div style="border: 2px solid #F44336; padding: 10px; border-radius: 5px;">
                        <h4>⭐ Calificación:</h4>
                        <p style="font-size: 1.2em; color: #F44336;"><strong>Reseña negativa 😡 ({calificacion}⭐)</strong></p>
                    </div>
                """, unsafe_allow_html=True)
        
        with col2:
            # Mostrar el análisis de sentimiento de VADER
            st.markdown("""
                <div style="border: 2px solid #4CAF50; padding: 10px; border-radius: 5px;">
                    <h4>📊 Análisis de Sentimiento (VADER):</h4>
                    <p><strong>Positivo:</strong> {pos:.2f}</p>
                    <p><strong>Neutral:</strong> {neu:.2f}</p>
                    <p><strong>Negativo:</strong> {neg:.2f}</p>
                </div>
            """.format(
                pos=pos,
                neu=neu,
                neg=neg
            ), unsafe_allow_html=True)

        # Distribuir la visualización en columnas
        col3, col4 = st.columns(2)

        # Definir valores y etiquetas antes de las columnas
        sentiment_values = [pos, neu, neg]
        sentiment_labels = ['Positivo', 'Neutral', 'Negativo']

        # Definir el sentimiento predominante para cambiar color de fondo
        sentiment_colors = {
            "Positivo": "#d4edda",
            "Neutral": "#fff3cd",
            "Negativo": "#f8d7da"
        }
        dominant_sentiment = sentiment_labels[sentiment_values.index(max(sentiment_values))]
        background_color = sentiment_colors[dominant_sentiment]

        with col3:
            st.markdown(f"""
                <div style="border: 2px solid black; padding: 10px; border-radius: 5px;">
                    <h4>📊 Análisis de Sentimientos</h4>
            """, unsafe_allow_html=True)

            # Gráfico de barras para análisis de sentimiento
            fig, ax = plt.subplots(figsize=(4, 3))
            bars = ax.bar(sentiment_labels, sentiment_values, color=['#4CAF50', '#FF9800', '#F44336'])

            # Agregar etiquetas a las barras
            for bar in bars:
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
                        f'{bar.get_height():.1f}', ha='center', fontsize=10, fontweight='bold')

            ax.set_ylabel("Proporción")
            ax.set_ylim(0, max(sentiment_values) * 1.2)  # Agregar margen superior

            st.pyplot(fig)

            st.markdown("</div>", unsafe_allow_html=True)  # Cerrar div del recuadro

        with col4:
            st.markdown(f"""
                <div style="border: 2px solid black; padding: 10px; border-radius: 5px;">
                    <h4>📊 Análisis de Sentimientos (Torta)</h4>
            """, unsafe_allow_html=True)

            # Gráfico de torta
            fig, ax = plt.subplots(figsize=(4, 3))  

            wedges, texts = ax.pie(
                sentiment_values,
                colors=['#4CAF50', '#FF9800', '#F44336'],
                startangle=90,
                wedgeprops={'edgecolor': 'black', 'linewidth': 1}  # Agregar borde a los sectores
            )

            ax.axis('equal')  # Mantener proporción del gráfico

            # Crear la leyenda con etiquetas y porcentajes fuera del gráfico
            total = sum(sentiment_values)
            legend_labels = [f"{label}: {value / total * 100:.1f}%" for label, value in zip(sentiment_labels, sentiment_values)]
            
            ax.legend(wedges, legend_labels, loc="center left", bbox_to_anchor=(1, 0.5), fontsize=9, frameon=False)

            st.pyplot(fig)

            st.markdown("</div>", unsafe_allow_html=True)  # Cerrar div del recuadro

        # Mostrar nube de palabras
        adjetivos_adverbios = extraer_palabras_clave(reseña)

        st.markdown(f"""
            <div style="border: 2px solid black; padding: 10px; border-radius: 5px; text-align: center;">
                <h4>📝 Nube de Palabras</h4>
        """, unsafe_allow_html=True)

        # Generar la nube de palabras solo con los adjetivos y adverbios
        wordcloud = WordCloud(width=400, height=200, background_color="white").generate(" ".join(adjetivos_adverbios))

#        Convertir la imagen a un array y mostrarla en Streamlit dentro del mismo recuadro
        st.image(wordcloud.to_array(), use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)

        # Distribuir el análisis de entidades en columnas
        col5, col6 = st.columns(2)
        # Aplicar estilo CSS para igualar la altura de las columnas
        st.markdown("""
            <style>
                .columna {
                    display: flex;
                    flex-direction: column;
                    height: 100%;
                }
            </style>
        """, unsafe_allow_html=True)

        with col5:
        # Agregar contorno con estilo CSS para las palabras clave
            if palabras_clave:
                st.markdown("""
                    <div style="border: 2px solid #4CAF50; padding: 10px; border-radius: 5px;">
                        <h4>🔑 Palabras Clave (Adjetivos y Adverbios):</h4>
                        <div style="display: flex; flex-wrap: wrap;">
                            """ + "\n".join([f"<span style='margin-right: 10px;'>{palabra}</span>" for palabra in palabras_clave]) + """
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div style="border: 2px solid #4CAF50; padding: 10px; border-radius: 5px;">
                        <h4>🔑 Palabras Clave (Adjetivos y Adverbios):</h4>
                        <p>No se encontraron adjetivos o adverbios en el texto.</p>
                    </div>
                """, unsafe_allow_html=True)


        with col6:
            # Aplicar NER al texto
            doc = nlp(reseña)
            entidades = [(ent.text, ent.label_) for ent in doc.ents]

            # Agregar contorno con estilo CSS solo después de extraer las entidades
            if entidades:
                st.markdown("""
                    <div style="border: 2px solid #4CAF50; padding: 10px; border-radius: 5px;">
                        <h4>🔍 Entidades Reconocidas:</h4>
                        <ul>
                            """ + "\n".join([f"<li><b>{entidad}</b> → {etiqueta}</li>" for entidad, etiqueta in entidades]) + """
                        </ul>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.info("No se encontraron entidades en el texto.")




    # Botón para volver a la página principal
    if st.button("Volver a la página principal"):
        st.session_state['pagina_actual'] = "principal"
        st.rerun()

# Lógica principal de la aplicación
def main():
    # Inicializar el estado de la sesión si no existe
    if 'pagina_actual' not in st.session_state:
        st.session_state['pagina_actual'] = "principal"

    # Mostrar la página correspondiente
    if st.session_state['pagina_actual'] == "principal":
        pagina_principal()
    elif st.session_state['pagina_actual'] == "resultados":
        pagina_resultados()

# Ejecutar la aplicación
if __name__ == "__main__":
    main()