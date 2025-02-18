# Análisis de Datos de Google Maps

Este proyecto se centra en el procesamiento y análisis de datos de reseñas de Google Maps. Se han combinado múltiples archivos CSV que contienen información de usuarios, reseñas y calificaciones de diferentes ubicaciones.

## Objetivos del Proyecto
- Unificar y limpiar los datos provenientes de diversas fuentes.
- Identificar valores nulos y decidir la mejor estrategia para manejarlos.
- Analizar la distribución de calificaciones y detectar posibles sesgos.
- Extraer insights a partir de las fechas y tendencias en las reseñas.

## Procesamiento de Datos
- Se han fusionado múltiples archivos CSV en un solo DataFrame.
- Se eliminaron columnas irrelevantes para el análisis, como `resp` y `pics`.
- Se identificaron y trataron valores nulos para mejorar la calidad de los datos.
- Se verificaron y eliminaron registros duplicados según `gmap_id`.

## Exploración de Datos
- Se analizó la distribución de ratings (1 a 5 estrellas).
- Se determinó el rango de fechas de las reseñas.
- Se identificaron patrones en los datos que podrían ser relevantes para estudios posteriores.

## Conclusiones
Este proceso ha permitido estructurar los datos de manera que puedan ser utilizados para futuros análisis y visualizaciones. Se pueden realizar estudios adicionales para detectar tendencias y patrones en las reseñas.

---

Si deseas contribuir o realizar análisis adicionales, puedes utilizar los archivos CSV procesados dentro del proyecto.

📦 yelp-google-reviews
│── 📄 README.md                 # Descripción del proyecto, instrucciones y equipo
│── 📄 requirements.txt          # Librerías necesarias para el proyecto
│
├── 📂 data                      # Datos del proyecto
│   ├── 📂 raw                   # Datos en bruto (sin procesar)
│   ├── 📂 processed             # Datos limpios y transformados
│   ├── 📂 external              # Datos de fuentes externas
│   ├── 📄 data_dictionary.md    # Diccionario de datos y explicaciones
│
├── 📂 notebooks                 # Notebooks Jupyter
│   ├── 📄 01_EDA.ipynb          # Análisis exploratorio de datos
│   ├── 📄 02_Feature_Selection.ipynb  # Selección de características
│   ├── 📄 03_Model_Training.ipynb  # Entrenamiento de modelos
│   ├── 📄 04_Model_Evaluation.ipynb  # Evaluación y métricas de modelos
│
├── 📂 src                       # Código fuente del proyecto
│   ├── 📂 data_preprocessing    # Scripts de limpieza y transformación de datos
│   ├── 📂 models                # Scripts de entrenamiento y evaluación de modelos
│   ├── 📂 visualization         # Scripts para generar gráficos y visualizaciones
│   ├── 📂 api                   # Código de la API (FastAPI o Flask)
│
├── 📂 app                       # Aplicación final o dashboard
│   ├── 📄 app.py                # Código principal de la aplicación
│   ├── 📂 static                # Archivos estáticos (CSS, imágenes, etc.)
│   ├── 📂 templates             # Plantillas HTML (si es necesario)
│
├── 📂 reports                   # Documentación y reportes
│   ├── 📄 final_report.pdf      # Informe final del proyecto
│   ├── 📄 presentation.pptx     # Presentación del proyecto
│   ├── 📄 results.md            # Resumen de los resultados obtenidos
│
├── 📂 tests                     # Pruebas y validaciones
│   ├── 📄 test_data_processing.py  # Pruebas de limpieza de datos
│   ├── 📄 test_model.py         # Pruebas de modelos de ML
│   ├── 📄 test_api.py           # Pruebas de la API
│
└── 📂 docs                      # Documentación técnica
    ├── 📄 project_overview.md   # Descripción técnica del proyecto
    ├── 📄 methodology.md        # Explicación de la metodología utilizada
    ├── 📄 team.md               # Información sobre los miembros del equipo
