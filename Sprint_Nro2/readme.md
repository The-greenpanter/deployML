# Proyecto Final Henry

## YELP & GOOGLE MAPS - REVIEWS AND RECOMMENDATIONS

### Sprint 2: Puesta en Marcha del Proyecto

### ✅ Data Cruda 
La fuente de información del proyecto fue proporcionada en Google Drive, los archivos originalmente proporcionados fueron los siguientes:

#### 🗂️ Google Maps:
- **metadata-sitios**: La carpeta tiene 11 archivos `.json` donde se dispone la metadata que contiene información del comercio, incluyendo localización, atributos y categorías.
- **review-estadosos**: Los archivos contienen las reviews de los usuarios, uno por cada estado de los EE.UU.

#### 🗂️ Yelp:
- **business**: Archivo `.pkl`, que contiene información del comercio, incluyendo localización, atributos y categorías.
- **review**: Archivo `.json` que contiene las reseñas completas, incluyendo el `user_id` que escribió el review y el `business_id` por el cual se escribe la reseña.
- **checkin**: Archivo `.json` que contiene los registros en el negocio.
- **tips**: Archivo `.json` con los Tips (consejos) escritos por el usuario. Los tips son más cortos que las reseñas y tienden a dar sugerencias rápidas.
- **Fuentes de datos**
diccionario de ruth
---

### ✅ Data Lake 
Se utiliza la plataforma Google Cloud, específicamente Cloud Storage, para organizar los datos en los siguientes buckets. Solo se tomó la información de los estados de Florida (FL), Nueva York (NY), Illinois (IL) y California (CL) para los años de 2016 a 2022.

#### 📂 Estructura del Data Lake:

---
 dataset-pf-gyelp/
 ├── ETL/
 │   ├── PreETL/
 ├── filtered/
 ├── Google Maps/
 │   ├── metadata-sitios/
 │   │   ├── processed/
 │   │   ├── raw/
 │   │   │   ├── datasets/
 │   ├── review-California/
 │   │   ├── processed/
 │   │   ├── raw/
 │   │   │   ├── datasets/
 ├── pipeline-root/
 │   ├── 619872001429/
 ├── Yelp/
 │   ├── processed/
 │   ├── raw/
```


#### 💾 Buckets en Cloud Storage:

- **`datos_crudos`**: Contiene los datos originales sin procesar. Los datos provienen de las fuentes explicadas anteriormente y se mantienen en este bucket antes de aplicarles cualquier transformación.
- **`datos_limpios`**: Contiene la data ya procesada y normalizada. Se divide en dos secciones:
  - **Datos de Google:**
    - Metadata del negocio: Donde se guarda toda la información sobre los negocios.
    - Reviews de negocios: Donde se almacenan las reseñas de los negocios.
  - **Datos de Yelp:**
    - Business: Contiene la información sobre los negocios de Yelp.
    - Reviews: Donde se almacenan todas las reseñas asociadas a los negocios de Yelp.
    - Users y Tips: Una tabla que contiene información sobre los usuarios y los tips que dejan en la plataforma.
- **`datos_nuevos`**: Este es el bucket donde se cargan nuevos archivos de datos. Cuando se suben archivos nuevos a este bucket, una Cloud Function se activa automáticamente, validando que el archivo tenga la estructura correcta y verificando si ya ha sido procesado. Si todo es correcto, procede a realizar las transformaciones necesarias.
- **`carga_incremental`**: Contiene los archivos nuevos normalizados después de correr las funciones de carga incremental.

---
```
### ✅ Automatización con Cloud Function
Para automatizar todo el proceso, se creó una ☁️ **Cloud Function** ☁️ que se ejecuta cuando se suben nuevos archivos al bucket `datos_nuevos`. Esta función:

1. Valida la estructura de los datos nuevos. 🆕
2. Verifica que los datos no existan previamente en el bucket `datos_limpios`. 🔃
3. Realiza las transformaciones necesarias. 🔄
4. Concatena los datos procesados con los que ya están en `datos_limpios`. ☑️
5. Finalmente, los datos transformados se cargan automáticamente en **BigQuery**.

---

### ✅ Carga Automática en BigQuery
Una vez que los datos están procesados y almacenados en `datos_limpios`, se envían automáticamente a **BigQuery**, donde se han creado las siguientes tablas para almacenar los datos de manera estructurada y facilitar su análisis posterior:

#### Para los datos de Google:
- **Tabla de Metadata del negocio**: Guarda toda la información relevante sobre los negocios.
- **Tabla de Reviews de negocios**: Almacena todas las reseñas de los negocios procesados.

#### Para los datos de Yelp:
- **Tabla de Business**: Contiene los datos de los negocios extraídos de Yelp.
- **Tabla de Reviews**: Almacena las reseñas asociadas a los negocios.
- **Tabla de Users y Tips**: Contiene información sobre los usuarios y los tips que dejan en la plataforma.

---

### ✅ Data Warehouse
De esta manera, se ha automatizado todo el flujo de trabajo **ETL**: desde la carga de archivos en Google Cloud Storage, la transformación de los datos mediante **Cloud Functions**, hasta la carga final en **BigQuery**, desde donde se pueden realizar consultas y análisis de forma rápida y eficiente.

#### 🔄 **Proceso ETL:**
- **Extracción (Extract)**: Los datos se extraen desde las fuentes originales, como Google Maps y Yelp a través de una API, y se almacenan en el bucket de `datos_crudos`.
- **Transformación (Transform)**: Las **Cloud Functions** validan, limpian y normalizan los datos automáticamente, y los colocan en los buckets de `datos_limpios` o `carga_incremental` según sea necesario.
- **Carga (Load)**: Los datos limpios se cargan automáticamente en **BigQuery** para análisis y consultas.

---

### ✅ Relacionamiento de Tablas
![Relación de tablas](https://example.com/relacion-tablas.png)

---

### ✅ Dashboard Mockup
El dashboard se realizará en 📊 **Power BI** 📊 y tendrá el siguiente esquema:

1. **Página de Inicio**: Presenta el menú principal del Dashboard con sus respectivos links de acceso a cada página.
2. **Resumen**: Presenta la información de los 4 principales KPI's así:
   - Valor Actual y % de cumplimiento de la meta 🎯.
   - Valor absoluto del indicador y distancia de este con el valor meta.
   - Gráfico de velocímetro 🏎️.
   - Gráfico de tendencia 📉.
3. **KPI's**: Cada KPI tendrá una página con gráficos de barras y otros elementos visuales.
4. **Mercado**: Contiene un contexto general del mercado gastronómico en los 4 estados 🗺️ seleccionados.

---

### ✅ Sistema de Recomendación
Para el modelo de recomendación se utilizará **Machine Learning**, específicamente el algoritmo de **Similitud del Coseno**. Esta técnica mide qué tan similares son dos elementos basándose en sus características. Un coseno cercano a **1** indica alta similitud, mientras que un coseno cercano a **0** indica baja similitud.

---
### Diccionario de Datos

Puedes acceder al diccionario de datos haciendo clic [aquí](https://docs.google.com/document/d/1dPeR2FKj-9TrlyMQnSwaY-1WtDi2RwgOfqhuOPikDkI/edit?usp=sharing).

¡Este proyecto sigue en desarrollo y se actualizará conforme avancemos en el sprint! 🚀
