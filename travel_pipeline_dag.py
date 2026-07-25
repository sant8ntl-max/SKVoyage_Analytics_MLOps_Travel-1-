"""Airflow DAG: retrain and refresh the flight price model on a schedule."""
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    "owner": "voyage-analytics",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}


def extract_data():
    print("Extracting latest flights/hotels/users data...")


def preprocess_data():
    print("Cleaning and feature-engineering the data...")


def train_model():
    print("Retraining the flight price regression model...")


def evaluate_model():
    print("Evaluating model against holdout set, logging to MLflow...")


def deploy_model():
    print("Promoting new model artifact and triggering Jenkins deploy...")


with DAG(
    dag_id="voyage_analytics_retraining_pipeline",
    default_args=default_args,
    description="Periodic retraining pipeline for the flight price model",
    schedule_interval="@weekly",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["voyage-analytics", "mlops"],
) as dag:

    t1 = PythonOperator(task_id="extract_data", python_callable=extract_data)
    t2 = PythonOperator(task_id="preprocess_data", python_callable=preprocess_data)
    t3 = PythonOperator(task_id="train_model", python_callable=train_model)
    t4 = PythonOperator(task_id="evaluate_model", python_callable=evaluate_model)
    t5 = PythonOperator(task_id="deploy_model", python_callable=deploy_model)

    t1 >> t2 >> t3 >> t4 >> t5
