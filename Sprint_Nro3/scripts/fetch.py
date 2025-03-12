from google.cloud import storage
import os
import requests
import csv
import pandas as pd

gcs_client = storage.Client()
BUCKET_NAME = "dataset-pf-gyelp"
RAW_FOLDER = "Yelp/airFlow/raw/"
PROCESSED_FOLDER = "Yelp/airFlow/processed/"

def save_to_csv(data, filename, folder):
    """Guarda los datos en un archivo CSV y lo sube a Google Cloud Storage."""
    local_path = f"/tmp/{filename}"  # Carpeta temporal en Airflow
    gcs_path = f"{folder}{filename}"  # Ruta en Google Cloud Storage

    # Guardar en CSV localmente
    df = pd.DataFrame(data)
    df.to_csv(local_path, index=False)

    # Subir a GCS
    bucket = gcs_client.bucket(BUCKET_NAME)
    blob = bucket.blob(gcs_path)
    blob.upload_from_filename(local_path)

    print(f"Archivo guardado en GCS: {BUCKET_NAME}/{gcs_path}")

def clear_bucket_folder(folder):
    """Elimina todos los archivos en una carpeta del bucket."""
    bucket = gcs_client.bucket(BUCKET_NAME)
    blobs = list(bucket.list_blobs(prefix=folder))
    
    if not blobs:
        print(f"No hay archivos en {BUCKET_NAME}/{folder} para eliminar.")
        return
    
    for blob in blobs:
        blob.delete()
    print(f"Se eliminaron {len(blobs)} archivos en {BUCKET_NAME}/{folder}")

def fetch_google_restaurants():
    """Obtiene datos de restaurantes de Google Places API y los guarda en un CSV."""
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {"query": "restaurants in California", "key": GOOGLE_API_KEY}
    response = requests.get(url, params=params)
    data = response.json()
    
    restaurants = [
        {"Business_ID": r.get("place_id"), "Name": r.get("name"), "Address": r.get("formatted_address"), "Rating": r.get("rating")} 
        for r in data.get("results", [])
    ]
    save_to_csv(restaurants, "google_restaurants.csv", RAW_FOLDER)

def fetch_yelp_restaurants():
    """Obtiene datos de restaurantes de Yelp API y los guarda en un CSV."""
    YELP_API_KEY = os.getenv("YELP_API_KEY")
    url = "https://api.yelp.com/v3/businesses/search"
    headers = {"Authorization": f"Bearer {YELP_API_KEY}"}
    params = {"location": "California", "term": "restaurants", "limit": 50}
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    
    restaurants = [
        {"Business_ID": b.get("id"), "Name": b.get("name"), "Address": ", ".join(b.get("location", {}).get("display_address", [])), "Rating": b.get("rating")} 
        for b in data.get("businesses", [])
    ]
    save_to_csv(restaurants, "yelp_restaurants.csv", RAW_FOLDER)

if __name__ == "__main__":
    # Limpiar los buckets antes de iniciar
    clear_bucket_folder(RAW_FOLDER)
    clear_bucket_folder(PROCESSED_FOLDER)

    # Ejecutar las funciones de recolección y procesamiento
    fetch_google_restaurants()
    fetch_yelp_restaurants()

