import pandas as pd
from google.cloud import bigquery, storage

SCHEMAS = {
    "dim_business": [
        bigquery.SchemaField("business_id", "STRING"),
        bigquery.SchemaField("name", "STRING"),
        bigquery.SchemaField("latitude", "FLOAT"),
        bigquery.SchemaField("longitude", "FLOAT"),
        bigquery.SchemaField("review_count", "INTEGER"),
    ],
    "dim_city": [
        bigquery.SchemaField("city_id", "STRING"),
        bigquery.SchemaField("city", "STRING"),
    ],
    "dim_category": [
        bigquery.SchemaField("category_id", "STRING"),
        bigquery.SchemaField("category", "STRING"),
    ],
}

# ConfiguraciÃ³n
BUCKET_NAME = "dataset-pf-gyelp"
PROCESSED_FOLDER = "Yelp/airFlow/processed"
DATASET_ID = "your_dataset_id"

# Mapeo de archivos a tablas
FILE_TABLE_MAPPING = {
    "dim_business.csv": "dim_business",
    "dim_city.csv": "dim_city",
    "dim_category.csv": "dim_category",
}

# Inicializar clientes
storage_client = storage.Client()
bq_client = bigquery.Client()

def load_to_bigquery():
    """Carga los archivos procesados desde GCS a BigQuery."""
    bucket = storage_client.bucket(BUCKET_NAME)
    blobs = list(bucket.list_blobs(prefix=PROCESSED_FOLDER))

    for blob in blobs:
        filename = blob.name.split("/")[-1]

        if not filename.endswith(".csv"):
            continue  # Ignorar archivos que no sean CSV

        table_name = FILE_TABLE_MAPPING.get(filename)

        if not table_name:
            print(f"âš ï¸ No se encontrÃ³ mapeo para {filename}, omitiendo...")
            continue

        local_path = f"/tmp/{filename}"
        blob.download_to_filename(local_path)

        df = pd.read_csv(local_path)

        # Convertir tipos de datos para evitar errores
        if table_name == "dim_business":
            df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
            df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")
            df["review_count"] = df["review_count"].astype("Int64")

        elif table_name == "dim_city":
            df["city_id"] = df["city_id"].astype(str)
            df["city"] = df["city"].astype(str)

        elif table_name == "dim_category":
            df["category_id"] = df["category_id"].astype(str)
            df["category"] = df["category"].astype(str)

        try:
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
            print(f"âœ… Datos cargados en {table_name} correctamente.")

        except Exception as e:
            print(f"âŒ Error al cargar {filename} en {table_name}: {e}")


if __name__ == "__main__":
    load_to_bigquery()
