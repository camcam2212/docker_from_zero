from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
import pandas as pd
import os
from datetime import datetime, timedelta

# Định nghĩa đường dẫn đến thư mục chứa các file CSV
CSV_FOLDER = 'D:\\intern_de\\csv'

# Định nghĩa DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 7, 26),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'csv_to_postgres',
    default_args=default_args,
    description='A simple DAG to load CSV data to PostgreSQL',
    schedule_interval=timedelta(days=1),
)

def load_csv_to_postgres():
    # Kết nối với PostgreSQL
    pg_hook = PostgresHook(postgres_conn_id='postgres')
    conn = pg_hook.get_conn()
    cursor = conn.cursor()

    # Lặp qua các file CSV trong thư mục
    for file_name in os.listdir(CSV_FOLDER):
        if file_name.endswith('.csv'):
            file_path = os.path.join(CSV_FOLDER, file_name)
            
            # Đọc file CSV
            df = pd.read_csv(file_path)
            
            # Lặp qua các hàng và chèn vào cơ sở dữ liệu
            for index, row in df.iterrows():
                cursor.execute(
                    "INSERT INTO your_table (Date, ID, Amount) VALUES (%s, %s, %s)",
                    (row['Date'], row['ID'], row['Amount'])
                )
    
    # Đóng kết nối
    conn.commit()
    cursor.close()
    conn.close()

# Định nghĩa tác vụ (task) để thực thi
load_csv_task = PythonOperator(
    task_id='load_csv_to_postgres',
    python_callable=load_csv_to_postgres,
    dag=dag,
)

# Chạy DAG
load_csv_task
