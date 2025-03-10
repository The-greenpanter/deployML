from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import transform
import load
import mapsETL  # 🔹 Importamos Maps

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 3, 9),
    'retries': 1,
}

dag = DAG(
    'etl_yelp_maps',  # 🔹 Cambiamos el nombre para reflejar ambas fuentes
    default_args=default_args,
    description='Pipeline ETL para Yelp y Google Maps con Airflow',
    schedule_interval='@weekly',
    catchup=False,
)

transform_yelp_task = PythonOperator(
    task_id='transform_yelp_data',
    python_callable=transform.transform_data,
    dag=dag,
)

transform_maps_task = PythonOperator(  # 🔹 Nuevo operador para Maps
    task_id='transform_maps_data',
    python_callable=mapsETL.transform_and_load,
    dag=dag,
)

load_task = PythonOperator(
    task_id='load_to_datawarehouse',
    python_callable=load.load_to_datawarehouse,
    dag=dag,
)

# 🔹 Definimos el orden: Yelp y Maps primero, luego la carga final
[transform_yelp_task, transform_maps_task] >> load_task
