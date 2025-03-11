import os
import pandas as pd
from google.cloud import storage
from langdetect import detect

# Configuración de GCS
BUCKET_NAME = "dataset-pf-gyelp"
RAW_FOLDER = "Yelp/airFlow/raw/"
PROCESSED_FOLDER = "Yelp/airFlow/processed/"

storage_client = storage.Client()

# Definir mapeo de esquemas
COLUMN_MAPPING = {
    "google_restaurants.csv": {
        "Business_ID": "business_id",
        "Name": "business_name",
        "Address": "address",
        "City": "city",
        "Category": "category",
        "Latitude": "latitude",
        "Longitude": "longitude",
        "Review_Count": "review_count"
    },
    "yelp_restaurants.csv": {
        "Business_ID": "business_id",
        "Name": "business_name",
        "Address": "address",
        "City": "city",
        "Category": "category",
        "Latitude": "latitude",
        "Longitude": "longitude",
        "Review_Count": "review_count"
    }
}

def clear_bucket_folder(folder):
    """Elimina todos los archivos en una carpeta del bucket."""
    bucket = storage_client.bucket(BUCKET_NAME)
    blobs = list(bucket.list_blobs(prefix=folder))
    
    if not blobs:
        print(f"No hay archivos en {BUCKET_NAME}/{folder} para eliminar.")
        return
    
    for blob in blobs:
        blob.delete()
    print(f"Se eliminaron {len(blobs)} archivos en {BUCKET_NAME}/{folder}")

def download_from_bucket(blob_name, local_path):
    """Descarga un archivo desde Google Cloud Storage."""
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(blob_name)
    blob.download_to_filename(local_path)

def upload_to_bucket(local_path, destination_blob_name):
    """Sube un archivo procesado a Google Cloud Storage."""
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(local_path)

def process_data():
    """Procesa los archivos de Yelp y Google, limpiando y transformando los datos."""
    for filename in COLUMN_MAPPING.keys():
        raw_blob = f"{RAW_FOLDER}{filename}"
        local_path = filename

        # Descargar el archivo desde GCS
        download_from_bucket(raw_blob, local_path)

        # Leer CSV
        df = pd.read_csv(local_path)

        # Limpieza de datos
        df.dropna(inplace=True)
        df.drop_duplicates(subset=["Business_ID"], inplace=True)
        df = df[df["Name"].apply(lambda x: detect(str(x)) in ["en", "es"])]

        # Transformación de columnas
        df.rename(columns=COLUMN_MAPPING[filename], inplace=True)

        # Guardar archivo transformado
        processed_filename = f"processed_{filename}"
        df.to_csv(processed_filename, index=False)

        # Subir archivo procesado a GCS
        processed_blob = f"{PROCESSED_FOLDER}{processed_filename}"
        upload_to_bucket(processed_filename, processed_blob)

        print(f"Archivo {processed_filename} procesado y subido a {processed_blob}")

if __name__ == "__main__":
    # Limpiar los buckets antes de procesar los datos
    clear_bucket_folder(PROCESSED_FOLDER)
    process_data()
