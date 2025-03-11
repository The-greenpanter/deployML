from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from scripts.fetch import fetch_and_upload
from scripts.process import transform_data
from scripts.load import load_to_datawarehouse

# Definir los argumentos del DAG
default_args = {
    "owner": "airflow",
    "start_date": datetime(2024, 7, 10),
    "retries": 5,
    "retry_delay": timedelta(minutes=5),
    "depends_on_past": False,
}

# Definir tareas
fetch_task = PythonOperator(
    task_id="fetch_data",
    python_callable=fetch_and_upload,
    dag=None,  # Se asignará después
)

transform_task = PythonOperator(
    task_id="transform_data",
    python_callable=transform_data,
    dag=None,
)

load_task = PythonOperator(
    task_id="load_to_datawarehouse",
    python_callable=load_to_datawarehouse,
    dag=None,
)

# Definir DAG después de las tareas
dag = DAG(
    "etl_yelp_maps",
    default_args=default_args,
    description="Pipeline ETL para Yelp y Google Maps con Airflow",
    schedule_interval="@weekly",
    catchup=False,  # Evita ejecuciones históricas
)

# Asignar el DAG a las tareas
fetch_task.dag = dag
transform_task.dag = dag
load_task.dag = dag

# Definir dependencias
fetch_task >> transform_task >> load_task
