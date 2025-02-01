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
