import pandas as pd
import numpy as np
import io
from google.cloud import storage
import hashlib

# Mapeo de columnas corregido (antes estaba invertido)
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

BUCKET_NAME = "dataset-pf-gyelp"
PROCESSED_FOLDER = "Yelp/airFlow/processed"

def generate_md5(value):
    return hashlib.md5(value.encode()).hexdigest()

def load_file_from_gcs(bucket, file_path):
    blob = bucket.blob(file_path)
    content = blob.download_as_text()
    return pd.read_csv(io.StringIO(content))

def save_dataframe_to_gcs(bucket, df, destination_path):
    blob = bucket.blob(destination_path)
    blob.upload_from_string(df.to_csv(index=False), content_type="text/csv")

def transform_data():
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)

    raw_files = ["google_restaurants.csv", "yelp_restaurants.csv"]
    dataframes = [load_file_from_gcs(bucket, f"Yelp/airFlow/raw/{file}") for file in raw_files]
    
    # ✅ Verificar columnas cargadas
    for file, df in zip(raw_files, dataframes):
        print(f"Columnas en {file}: {df.columns.tolist()}")

    # ✅ Aplicar el mapeo correctamente
    df = pd.concat(dataframes, ignore_index=True)
    df.rename(columns={k: v for file_map in COLUMN_MAPPING.values() for k, v in file_map.items()}, inplace=True)

    # ✅ Normalización de ciudades y categorías (Verifica si existen antes de operar)
    if 'city' in df.columns:
        cities = df[['city']].drop_duplicates().copy()
        cities['city_id'] = cities['city'].apply(generate_md5)
    else:
        print("⚠️ La columna 'city' no existe en el DataFrame.")
        cities = pd.DataFrame(columns=['city', 'city_id'])

    if 'category' in df.columns:
        categories = df[['category']].drop_duplicates().copy()
        categories['category_id'] = categories['category'].apply(generate_md5)
    else:
        print("⚠️ La columna 'category' no existe en el DataFrame.")
        categories = pd.DataFrame(columns=['category', 'category_id'])

    # ✅ Solo hacer el merge si la columna existe
    if 'city' in df.columns:
        df = df.merge(cities, on='city', how='left').drop(columns=['city'], errors='ignore')

    if 'category' in df.columns:
        df = df.merge(categories, on='category', how='left').drop(columns=['category'], errors='ignore')

    transformed_data = {
        "dim_business": df[['business_id', 'business_name', 'address', 'city_id', 'category_id', 'latitude', 'longitude', 'review_count']],
        "dim_city": cities[['city_id', 'city']],
        "dim_category": categories.rename(columns={'category': 'category'})
    }

    for name, df in transformed_data.items():
        save_dataframe_to_gcs(bucket, df, f"{PROCESSED_FOLDER}/{name}.csv")

    print("✅ Transformación completada y guardada en processed.")
