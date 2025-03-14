import logging
import json
import csv
import io
import requests
import pandas as pd
from airflow.models import Variable
from airflow.providers.google.cloud.hooks.gcs import GCSHook

BUCKET_NAME = "dataset-pf-gyelp"
RAW_FOLDER = "Yelp/airFlow/raw/"
PROCESSED_FOLDER = "Yelp/airFlow/processed/"
gcs_hook = GCSHook(gcp_conn_id="google_cloud_default")  # Conexión a GCS

def save_to_gcs(data, filename):
    """Guarda un JSON en GCS como un archivo CSV."""
    if not data:
        logging.warning(f"⚠️ No hay datos para guardar en {filename}")
        return
    
    # Obtener las claves para las columnas del CSV
    keys = data[0].keys() if data else ["Business_ID", "Name", "Address", "Rating"]
    
    # Convertir datos a CSV en memoria
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=keys)
    writer.writeheader()
    writer.writerows(data)
    
    # Subir a GCS
    gcs_path = f"{RAW_FOLDER}{filename.replace('.json', '.csv')}"
    gcs_hook.upload(BUCKET_NAME, gcs_path, data=output.getvalue(), mime_type="text/csv")
    
    logging.info(f"✅ Archivo guardado en GCS: gs://{BUCKET_NAME}/{gcs_path}")

def clear_bucket_folder(folder):
    """Elimina todos los archivos en una carpeta del bucket."""
    blobs = gcs_hook.list(BUCKET_NAME, prefix=folder)
    if not blobs:
        logging.info(f"📂 No hay archivos en {BUCKET_NAME}/{folder} para eliminar.")
        return
    
    for blob in blobs:
        gcs_hook.delete(BUCKET_NAME, blob)
    
    logging.info(f"🗑️ Se eliminaron {len(blobs)} archivos en {BUCKET_NAME}/{folder}")

def fetch_google_restaurants():
    """Obtiene datos de Google Places API y los guarda en GCS."""
    
    # 🔹 Obtener API Key desde Airflow Variables
    GOOGLE_API_KEY = Variable.get("GOOGLE_API_KEY", default_var=None)
    if not GOOGLE_API_KEY:
        logging.error("❌ La variable GOOGLE_API_KEY no está configurada en Airflow.")
        return

    # 🔹 Configurar URL y parámetros
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {"query": "restaurants in California", "key": GOOGLE_API_KEY}
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Lanza una excepción si hay errores HTTP
    except requests.exceptions.RequestException as e:
        logging.error(f"❌ Error al hacer la petición a la API de Google Places: {e}")
        return

    # 🔹 Procesar la respuesta
    data = response.json()
    logging.info(f"📊 Google API Response: {json.dumps(data, indent=2)}")

    # 🔹 Extraer datos relevantes
    restaurants = [
        {
            "Business_ID": r.get("place_id"),
            "Name": r.get("name"),
            "Address": r.get("formatted_address"),
            "City": r.get("plus_code", {}).get("compound_code", "").split(" ")[-1] if r.get("plus_code") else "Unknown",
            "Category": r["types"][0] if r.get("types") else "Unknown",
            "Latitude": r["geometry"]["location"]["lat"],
            "Longitude": r["geometry"]["location"]["lng"],
            "Review_Count": r.get("user_ratings_total", 0),
        }
        for r in data.get("results", [])
    ]

    if not restaurants:
        logging.warning("⚠️ Google API devolvió una lista vacía")
    
    # 🔹 Guardar en Google Cloud Storage (GCS)
    save_to_gcs(restaurants, "google_restaurants.json")

def fetch_yelp_restaurants():
    """Obtiene datos de Yelp API y los guarda en GCS."""
    YELP_API_KEY = Variable.get("YELP_API_KEY", default_var=None)
    if not YELP_API_KEY:
        logging.error("❌ La variable YELP_API_KEY no está configurada en Airflow.")
        return

    url = "https://api.yelp.com/v3/businesses/search"
    headers = {"Authorization": f"Bearer {YELP_API_KEY}"}
    params = {"location": "California", "term": "restaurants", "limit": 50}

    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        logging.error(f"❌ Error en la API de Yelp: {response.status_code} - {response.text}")
        return

    data = response.json()
    logging.info(f"📊 Yelp API Response: {json.dumps(data, indent=2)}")

    # Validar si "businesses" existe y no está vacío
    if "businesses" not in data or not isinstance(data["businesses"], list) or not data["businesses"]:
        logging.warning("⚠️ Yelp API devolvió una lista vacía o con formato incorrecto.")
        return

    restaurants = []
    for r in data["businesses"]:
        # Validaciones de cada clave antes de acceder a ellas
        business_id = r.get("id", None)
        name = r.get("name", None)
        review_count = r.get("review_count", None)

        # Validar ubicación
        location = r.get("location", {})
        address = ", ".join(location.get("display_address", [])) if isinstance(location.get("display_address"), list) else None
        city = location.get("city", None)

        # Validar categorías
        categories = r.get("categories", [])
        category = ", ".join([c.get("title", "") for c in categories if isinstance(c, dict)]) if categories else None

        # Validar coordenadas
        coordinates = r.get("coordinates", {})
        latitude = coordinates.get("latitude", None)
        longitude = coordinates.get("longitude", None)

        restaurant_info = {
            "Business_ID": business_id,
            "Name": name,
            "Address": address,
            "City": city,
            "Category": category,
            "Latitude": latitude,
            "Longitude": longitude,
            "Review_Count": review_count
        }

        restaurants.append(restaurant_info)

    # Verificar si hay datos antes de guardar
    if not restaurants:
        logging.warning("⚠️ No se extrajeron datos válidos de la API.")
        return

    # Guardar en un archivo CSV para depuración
    df = pd.DataFrame(restaurants)
    df.to_csv("/tmp/yelp_restaurants.csv", index=False)
    logging.info("✅ Datos de Yelp guardados en /tmp/yelp_restaurants.csv")

    # Guardar en GCS (asumiendo que tienes la función implementada)
    save_to_gcs(restaurants, "yelp_restaurants.json")

if __name__ == "__main__":
    fetch_google_restaurants()
    fetch_yelp_restaurants()
