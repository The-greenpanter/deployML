from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from scripts.process import transform_data
from scripts.load import load_to_datawarehouse
from scripts.mapsETL import transform_and_load

default_args = {
    "owner": "airflow",
    "start_date": days_ago(1),
    "retries": 5,
}

dag = DAG(
    'etl_yelp_maps',
    default_args=default_args,
    description='Pipeline ETL para Yelp y Google Maps con Airflow',
    schedule_interval='@weekly',
    catchup=True,
)

transform_yelp_task = PythonOperator(
    task_id='transform_yelp_data',
    python_callable=transform_data,
    dag=dag,
)

transform_maps_task = PythonOperator(
    task_id='transform_maps_data',
    python_callable=transform_and_load,
    dag=dag,
)

load_task = PythonOperator(
    task_id='load_to_datawarehouse',
    python_callable=load_to_datawarehouse,
    dag=dag,
)

[transform_yelp_task, transform_maps_task] >> load_task
