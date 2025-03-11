import os
import requests
import csv
import time
import json
from google.cloud import storage

# Configurar la autenticación con la clave de servicio JSON
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "proyectofinalgogleyelp-41e96ec7a40a.json"

# Configuración de APIs (REEMPLAZAR CON TUS KEYS)
GOOGLE_API_KEY = "AIzaSyBVFqawIp7wy2kTnY7ZVt9veOS7-yKfohU""
YELP_API_KEY = "81MeibfW8d_OHhY9oRupbSWAy3cBuNrvOZJPNC3hQWkPa-ZFMIdDKeN3_pu6G8cVOvbR-1r8hIPxWqQV_u56wDQPPHr4kDve44nvtlxE7e3RMrq2M72jXM9ZXwTPZ3Yx"


# Configuración de buckets
temp_bucket = "dataset-pf-gyelp-temporal"
final_bucket = "dataset-pf-gyelp"
storage_client = storage.Client()

def clear_bucket(bucket_name):
    """Elimina todos los archivos dentro de un bucket de GCP."""
    bucket = storage_client.bucket(bucket_name)
    blobs = bucket.list_blobs()
    for blob in blobs:
        blob.delete()
    print(f"Se han eliminado todos los archivos en {bucket_name}")

def fetch_google_restaurants(location="California", pages=3):
    base_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    restaurants = []
    next_page_token = None
    
    for _ in range(pages):
        params = {
            "query": "restaurants in " + location,
            "key": GOOGLE_API_KEY,
            "type": "restaurant",
            "language": "es",
            "pagetoken": next_page_token if next_page_token else ""
        }
        
        response = requests.get(base_url, params=params)
        data = response.json()
        
        for result in data.get("results", []):
            restaurants.append({
                "Gmap_id": result.get("place_id"),
                "Nombre": result.get("name"),
                "Address": result.get("formatted_address"),
                "Avg_rating": result.get("rating"),
                "Reseñas": result.get("user_ratings_total"),
                "Latitud": result.get("geometry", {}).get("location", {}).get("lat"),
                "Longitud": result.get("geometry", {}).get("location", {}).get("lng"),
                "Fuente": "Google Maps"
            })
        
        next_page_token = data.get("next_page_token")
        if not next_page_token:
            break
        time.sleep(2)
    
    return restaurants

def fetch_yelp_restaurants(location="California"):
    url = "https://api.yelp.com/v3/businesses/search"
    headers = {"Authorization": f"Bearer {YELP_API_KEY}"}
    params = {
        "location": location,
        "term": "restaurants",
        "limit": 50
    }
    
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    
    return [{
        "Nombre": business.get("name"),
        "Address": ", ".join(business.get("location", {}).get("display_address", [])),
        "Avg_rating": business.get("rating"),
        "Reseñas": business.get("review_count"),
        "Latitud": business.get("coordinates", {}).get("latitude"),
        "Longitud": business.get("coordinates", {}).get("longitude"),
        "Fuente": "Yelp"
    } for business in data.get("businesses", [])]

def save_to_csv(data, filename):
    if not data:
        return
    
    keys = data[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)

def upload_to_gcs(bucket_name, source_file_name, destination_blob_name):
    """Sube un archivo a Google Cloud Storage."""
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    print(f"Archivo {source_file_name} subido a {bucket_name}/{destination_blob_name}")

# Ejecución principal
if __name__ == "__main__":
    try:
        print("Limpiando buckets...")
        clear_bucket(temp_bucket)
        clear_bucket(final_bucket)

        print("Obteniendo datos de Google Maps...")
        google_data = fetch_google_restaurants(pages=3)
        print("Obteniendo datos de Yelp...")
        yelp_data = fetch_yelp_restaurants()

        google_filename = "google_restaurants.csv"
        yelp_filename = "yelp_restaurants.csv"
        save_to_csv(google_data, google_filename)
        save_to_csv(yelp_data, yelp_filename)

        print("Subiendo archivos a GCS...")
        upload_to_gcs(temp_bucket, google_filename, f"Yelp/processed/{google_filename}")
        upload_to_gcs(temp_bucket, yelp_filename, f"Yelp/processed/{yelp_filename}")

        print("Proceso completado.")
    except Exception as e:
        print(f"Error: {str(e)}")
