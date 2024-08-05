from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import psycopg2
from psycopg2.extras import execute_values

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 8, 5),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'etl_pipeline',
    default_args=default_args,
    description='A simple ETL pipeline',
    schedule_interval=timedelta(days=1),
)

# Function to perform the ETL
def etl():
    # Database connection details
    SOURCE_HOST = 'intern_de-postgres-1'  # Assuming your Docker container is on localhost
    SOURCE_DATABASE = 'airflow'  # Replace with your source database name
    SOURCE_USER = 'airflow'  # Replace with your source username
    SOURCE_PASSWORD = 'airflow'  # Replace with your source password
    SOURCE_PORT = 5432  # Replace with your source port if different

    TARGET_HOST = 'intern_de-postgres-1'
    TARGET_DATABASE = 'airflow'
    TARGET_USER = 'airflow'
    TARGET_PASSWORD = 'airflow'
    TARGET_PORT = 5432

    # Connect to the source database
    source_conn = psycopg2.connect(
        host=SOURCE_HOST,
        database=SOURCE_DATABASE,
        user=SOURCE_USER,
        password=SOURCE_PASSWORD,
        port=SOURCE_PORT
    )

    # Connect to the target database
    target_conn = psycopg2.connect(
        host=TARGET_HOST,
        database=TARGET_DATABASE,
        user=TARGET_USER,
        password=TARGET_PASSWORD,
        port=TARGET_PORT
    )

    source_cursor = source_conn.cursor()
    target_cursor = target_conn.cursor()

    # Fetch data from the source view
    source_cursor.execute("SELECT id, based_date, amount, quantity FROM vw_agg_invoice")
    data = source_cursor.fetchall()

    # Create the target table if it doesn't exist
    create_table_query = """
    CREATE TABLE IF NOT EXISTS agg_invoice (
        id BIGINT PRIMARY KEY,
        based_date DATE,
        amount BIGINT,
        quantity BIGINT
    )
    """
    target_cursor.execute(create_table_query)

    # Insert data into the target table
    insert_query = """
    INSERT INTO agg_invoice (id, based_date, amount, quantity)
    VALUES %s
    ON CONFLICT (id) DO NOTHING
    """

    execute_values(target_cursor, insert_query, data)

    # Commit the transaction
    target_conn.commit()

    # Close the connections
    source_cursor.close()
    source_conn.close()
    target_cursor.close()
    target_conn.close()

    print("ETL process completed successfully!")

# Define the PythonOperator task
etl_task = PythonOperator(
    task_id='etl_task',
    python_callable=etl,
    dag=dag,
)

# Set the task dependencies
etl_task
