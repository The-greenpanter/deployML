# README: Configuración y Uso de DAGs en Apache Airflow

## Descripción del Proyecto
Este proyecto implementa DAGs en Apache Airflow para la extracción, transformación y carga (ETL) de datos en un entorno de BigQuery. Se han definido diferentes tareas dentro de los DAGs para garantizar una ingesta de datos eficiente y estructurada.

## Estructura de los DAGs
### 1. Extracción de Datos
- Se obtienen datos desde diversas fuentes como archivos CSV, bases de datos externas o APIs.
- Los datos extraídos se almacenan temporalmente en un bucket de almacenamiento en la nube o una base de datos intermedia.

### 2. Transformación de Datos
- Se normalizan y limpian los datos.
- Se estructuran en diferentes tablas dimensionadas como `dim_user`, `dim_business`, `dim_city` y `dim_category`.
- Se genera una tabla de hechos `fact_reviews` con la información combinada.

### 3. Carga en BigQuery
- Los datos procesados se suben a Google BigQuery en su estructura final.
- Se validan los esquemas de las tablas para evitar inconsistencias.

## Archivos Principales
- `dags/etl_pipeline.py`: Contiene la definición principal del DAG de ETL.
- `dags/utils.py`: Contiene funciones auxiliares como `generate_md5()` para la generación de claves.
- `dags/config.py`: Configuración de credenciales y rutas de almacenamiento.

## Dependencias
Para ejecutar los DAGs, asegúrese de tener instaladas las siguientes dependencias en su entorno de Airflow:

```bash
pip install apache-airflow[gcp]
pip install pandas google-cloud-bigquery
```

## Configuración en Airflow
1. Copiar los archivos a la carpeta `dags/` de Airflow.
2. Configurar las credenciales de GCP en `config.py` o en las variables de entorno de Airflow.
3. Activar los DAGs desde la UI de Airflow y monitorear su ejecución.

## Solución de Problemas
### 1. **Error: `category_id` no encontrado en `fact_reviews`**
   - Solución: Se modificó la transformación de datos para agregar `category_id` mediante un `merge` con `business_cleaned`.

### 2. **Error de conexión con BigQuery**
   - Verificar que las credenciales de GCP estén correctamente configuradas.
   - Confirmar que la cuenta de servicio tenga permisos de escritura en BigQuery.

## Contribuciones
Cualquier mejora o corrección puede ser enviada mediante pull requests en el repositorio correspondiente.

---
Este documento servirá como guía para la configuración y mantenimiento del flujo de datos en Apache Airflow.

