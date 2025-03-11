import requests
import csv
import time
import json
import googlemaps


# Configuración de APIs (REEMPLAZAR CON TUS KEYS)
GOOGLE_API_KEY = "AIzaSyBVFqawIp7wy2kTnY7ZVt9veOS7-yKfohU"
YELP_API_KEY = "81MeibfW8d_OHhY9oRupbSWAy3cBuNrvOZJPNC3hQWkPa-ZFMIdDKeN3_pu6G8cVOvbR-1r8hIPxWqQV_u56wDQPPHr4kDve44nvtlxE7e3RMrq2M72jXM9ZXwTPZ3Yx"

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
                "Nombre": result.get("name"),
                "Dirección": result.get("formatted_address"),
                "Rating": result.get("rating"),
                "Reseñas": result.get("user_ratings_total"),
                "Latitud": result.get("geometry", {}).get("location", {}).get("lat"),
                "Longitud": result.get("geometry", {}).get("location", {}).get("lng"),
                "Fuente": "Google Maps"
            })
        
        next_page_token = data.get("next_page_token")
        if not next_page_token:
            break
        time.sleep(2)  # Necesario para paginación de Google
    
    return restaurants

def fetch_yelp_restaurants(location="California"):
    url = "https://api.yelp.com/v3/businesses/search"
    headers = {"Authorization": f"Bearer {YELP_API_KEY}"}
    params = {
        "location": location,
        "term": "restaurants",
        "limit": 50  # Límite máximo permitido por Yelp
    }
    
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    
    return [{
        "Nombre": business.get("name"),
        "Dirección": ", ".join(business.get("location", {}).get("display_address", [])),
        "Rating": business.get("rating"),
        "Reseñas": business.get("review_count"),
        "Latitud": business.get("coordinates", {}).get("latitude"),
        "Longitud": business.get("coordinates", {}).get("longitude"),
        "Precio": business.get("price"),
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

# Ejecución principal
if __name__ == "__main__":
    try:
        print("Obteniendo datos de Google Maps...")
        google_data = fetch_google_restaurants(pages=3)  # ~60 resultados
        
        print("Obteniendo datos de Yelp...")
        yelp_data = fetch_yelp_restaurants()  # 50 resultados
        
        datagoogle = google_data
        datayelp = yelp_data
        print(f"Total de restaurantes obtenidos: {len(datagoogle)}")
        print(f"Total de restaurantes obtenidos: {len(datayelp)}")
        save_to_csv(datagoogle, "restaurantes_california.csv")
        save_to_csv(datayelp, "restaurantes_californiayelp.csv")
        print("Datos guardados en restaurantes_california.csv")
        
    except Exception as e:
        print(f"Error: {str(e)}")