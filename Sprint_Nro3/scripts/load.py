from google.cloud import bigquery, storage
import pandas as pd
import os

# Configuración
BUCKET_NAME = "dataset-pf-gyelp"
PROCESSED_FOLDER = "Yelp/airFlow/processed/"
DATASET_ID = "yelp_dataset"

# Inicializar clientes
storage_client = storage.Client()
bq_client = bigquery.Client()

# Definir esquemas de BigQuery
SCHEMAS = {
    "dim_category": [
        bigquery.SchemaField("category_id", "STRING"),
        bigquery.SchemaField("category", "STRING"),
    ],
    "dim_city": [
        bigquery.SchemaField("city_id", "STRING"),
        bigquery.SchemaField("city", "STRING"),
    ],
    "dim_business": [
        bigquery.SchemaField("business_id", "STRING"),
        bigquery.SchemaField("business_name", "STRING"),
        bigquery.SchemaField("address", "STRING"),
        bigquery.SchemaField("city_id", "STRING"),
        bigquery.SchemaField("category_id", "STRING"),
        bigquery.SchemaField("latitude", "FLOAT64"),
        bigquery.SchemaField("longitude", "FLOAT64"),
        bigquery.SchemaField("review_count", "INT64"),
    ],
    "fact_reviews": [
        bigquery.SchemaField("review_id", "STRING"),
        bigquery.SchemaField("business_id", "STRING"),
        bigquery.SchemaField("user_id", "STRING"),
        bigquery.SchemaField("category_id", "STRING"),
        bigquery.SchemaField("review_date", "DATE"),
        bigquery.SchemaField("stars", "INT64"),
        bigquery.SchemaField("text", "STRING"),
    ],
    "dim_user": [
        bigquery.SchemaField("user_id", "STRING"),
        bigquery.SchemaField("name", "STRING"),
        bigquery.SchemaField("review_count", "INT64"),
        bigquery.SchemaField("yelping_since", "DATE"),
    ]
}

# Mapeo de nombres de archivos a tablas en BigQuery
FILE_TABLE_MAPPING = {
    "processed_google_restaurants.csv": "dim_business",
    "processed_yelp_restaurants.csv": "dim_business",
    "processed_reviews.csv": "fact_reviews",
    "processed_users.csv": "dim_user",
    "processed_categories.csv": "dim_category",
    "processed_cities.csv": "dim_city"
}

def check_dataset():
    """Verifica si el dataset existe en BigQuery y lo crea si no."""
    dataset_ref = bq_client.dataset(DATASET_ID)
    try:
        bq_client.get_dataset(dataset_ref)
        print(f"✅ Dataset {DATASET_ID} encontrado en BigQuery.")
    except Exception:
        print(f"⚠️ Dataset {DATASET_ID} no encontrado. Creándolo...")
        dataset = bigquery.Dataset(dataset_ref)
        dataset.location = "US"
        bq_client.create_dataset(dataset)
        print(f"✅ Dataset {DATASET_ID} creado.")

def clean_existing_data(table_name):
    """Limpia los datos previos en la tabla de BigQuery antes de cargar nuevos datos."""
    query = f"DELETE FROM `{bq_client.project}.{DATASET_ID}.{table_name}` WHERE TRUE"
    query_job = bq_client.query(query)
    query_job.result()  # Espera a que termine
    print(f"🗑️ Datos previos eliminados de {table_name}")

def load_to_bigquery():
    """Carga los archivos procesados desde GCS a BigQuery."""
    check_dataset()  # Verificar si el dataset existe

    bucket = storage_client.bucket(BUCKET_NAME)
    blobs = list(bucket.list_blobs(prefix=PROCESSED_FOLDER))

    for blob in blobs:
        filename = blob.name.split("/")[-1]

        if not filename.endswith(".csv"):
            continue  # Ignorar archivos que no sean CSV

        table_name = FILE_TABLE_MAPPING.get(filename)

        if not table_name:
            print(f"⚠️ No se encontró mapeo para {filename}, omitiendo...")
            continue

        local_path = f"/tmp/{filename}"
        blob.download_to_filename(local_path)

        df = pd.read_csv(local_path)

        # Convertir tipos de datos para evitar errores
        if table_name == "dim_business":
            df["latitude"] = df["latitude"].astype(float)
            df["longitude"] = df["longitude"].astype(float)
            df["review_count"] = df["review_count"].astype("Int64")  # Soporta valores nulos

        if table_name == "fact_reviews":
            df["stars"] = df["stars"].astype("Int64")
            df["review_date"] = pd.to_datetime(df["review_date"]).dt.date  # Convertir a formato DATE

        if table_name == "dim_user":
            df["review_count"] = df["review_count"].astype("Int64")
            df["yelping_since"] = pd.to_datetime(df["yelping_since"]).dt.date  # Convertir a DATE

        try:
            # Limpiar datos previos en la tabla antes de cargar nuevos
            clean_existing_data(table_name)

            # Cargar datos a BigQuery
            table_ref = bq_client.dataset(DATASET_ID).table(table_name)
            job = bq_client.load_table_from_dataframe(
                df, 
                table_ref, 
                job_config=bigquery.LoadJobConfig(
                    schema=SCHEMAS[table_name], 
                    write_disposition="WRITE_APPEND"
                )
            )
            job.result()  # Esperar a que termine
            print(f"✅ Datos cargados en {table_name} correctamente.")

        except Exception as e:
            print(f"❌ Error al cargar {filename} en {table_name}: {e}")

if __name__ == "__main__":
    load_to_bigquery()
