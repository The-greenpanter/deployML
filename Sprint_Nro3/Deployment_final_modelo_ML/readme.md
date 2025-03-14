# Proyecto de Análisis de Reseñas y Reconocimiento de Entidades (NER)

## Descripción
Este proyecto tiene como objetivo analizar reseñas de restaurantes utilizando procesamiento de lenguaje natural (NLP). Se han desarrollado dos modelos:
1. Un modelo de análisis de sentimientos y calificaciones.
2. Un modelo de reconocimiento de entidades (NER) entrenado para detectar términos relevantes en las reseñas.

## Tecnologías Utilizadas
- **Python**: Lenguaje principal del proyecto.
- **spaCy**: Para el entrenamiento del modelo NER.
- **Streamlit**: Para la visualización interactiva de las reseñas.
- **Pandas**: Para el procesamiento y manipulación de datos.
- **Matplotlib y Seaborn**: Para la visualización de datos.
- **WordCloud**: Para la generación de nubes de palabras basadas en las reseñas.

## Modelos Implementados

### 1. Modelo de Análisis de Reseñas
Este modelo permite a los usuarios seleccionar reseñas de un dataset y visualizar la calificación correspondiente mediante estrellas.
- Extrae la reseña y la calificación desde un archivo CSV.
- Muestra la reseña seleccionada con su calificación en una página de resultados.
Se ha entrenado un modelo de spaCy para identificar entidades en las reseñas.
- **Entidades detectadas**: Nombres de comidas, adjetivos descriptivos, emociones y aspectos del servicio.
- **Proceso de entrenamiento**: Se han etiquetado manualmente reseñas y entrenado el modelo en ellas.
- **Aplicaciones**: Extracción de información clave para entender mejor la percepción de los clientes.

### 2.  Modelo 2: Top 10 de cada ciudad
Este modelo permite a los usuarios seleccionar reseñas de un dataset y visualiza las cordenadas de cada restaurante.
- Top 10 restaurantes en esa ciudad.
- Categoría de cada uno.
- Ubicación en un mapa interactivo.
- Análisis de tendencia gastronómica en la ciudad.

