import pandas as pd
import numpy as np
import os
from google.cloud import storage

# Mapeo de columnas
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

def transform_data():
    """Carga archivos de restaurantes, los transforma y los almacena en processed."""
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)

    # Cargar los archivos
    raw_files = ["google_restaurants.csv", "yelp_restaurants.csv"]
    dataframes = [load_file_from_gcs(bucket, f"Yelp/airFlow/raw/{file}") for file in raw_files]

    # Unir datasets y mapear columnas
    df = pd.concat(dataframes, ignore_index=True)
    df.rename(columns={v: k for file_map in COLUMN_MAPPING.values() for k, v in file_map.items()}, inplace=True)

    # 🔹 Normalización de ciudades y categorías
    cities = df[['city']].drop_duplicates().copy()
    cities['city_id'] = cities['city'].apply(generate_md5)

    categories = df[['category']].drop_duplicates().copy()
    categories['category_id'] = categories['category'].apply(generate_md5)

    # 🔹 Transformación de negocios
    df = df.merge(cities, on='city', how='left').drop(columns=['city'])
    df = df.merge(categories, on='category', how='left').drop(columns=['category'])

    # 🔹 Generar dataframes para cada esquema
    transformed_data = {
        "dim_business": df[['business_id', 'business_name', 'address', 'city_id', 'category_id', 'latitude', 'longitude', 'review_count']],
        "dim_city": cities[['city_id', 'city']],
        "dim_category": categories.rename(columns={'category': 'category'})
    }

    # Guardar archivos en processed
    for name, df in transformed_data.items():
        save_dataframe_to_gcs(bucket, df, f"{PROCESSED_FOLDER}/{name}.csv")

    print("✅ Transformación completada y guardada en processed.")
