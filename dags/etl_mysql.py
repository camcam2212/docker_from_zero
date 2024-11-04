from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import psycopg2
from psycopg2.extras import execute_values
import mysql.connector
from mysql.connector import Error

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 8, 5),
    'retries': 1, #The number of retries if a task fails
    'retry_delay': timedelta(minutes=5), #The delay between retries
}

# Define the DAG
dag = DAG(
    'etl_mysql',
    default_args=default_args,
    description='A simple ETL pipeline',
    schedule_interval=timedelta(days=1),
)

# Function to perform the ETL
def etl():
    # Database connection details
    SOURCE_HOST = 'intern_de-postgres-1'
    SOURCE_DATABASE = 'airflow'
    SOURCE_USER = 'airflow'
    SOURCE_PASSWORD = 'airflow'
    SOURCE_PORT = 5432

    TARGET_HOST = 'son-mysql'
    TARGET_DATABASE = 'mysql'
    TARGET_USER = 'root'
    TARGET_PASSWORD = 'airflow'
    TARGET_PORT = 3306

    # Connect to the source database (PostgreSQL)
    source_conn = psycopg2.connect(
        host=SOURCE_HOST,
        database=SOURCE_DATABASE,
        user=SOURCE_USER,
        password=SOURCE_PASSWORD,
        port=SOURCE_PORT
    )

    # Connect to the target database (MySQL)
    target_conn = mysql.connector.connect(
        host=TARGET_HOST,
        database=TARGET_DATABASE,
        user=TARGET_USER,
        password=TARGET_PASSWORD,
        port=TARGET_PORT
    )

    source_cursor = source_conn.cursor()
    target_cursor = target_conn.cursor()

    try:
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
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            based_date=VALUES(based_date),
            amount=VALUES(amount),
            quantity=VALUES(quantity)
        """
        
        # Use executemany to insert the data
        target_cursor.executemany(insert_query, data)

        # Commit the transaction
        target_conn.commit()

        print("ETL process completed successfully!")
    
    except Error as e:
        print(f"Error: {e}")
        target_conn.rollback()
    
    finally:
        # Close the connections
        source_cursor.close()
        source_conn.close()
        target_cursor.close()
        target_conn.close()

# Define the PythonOperator task
etl_task = PythonOperator(
    task_id='etl_task',
    python_callable=etl,
    dag=dag,
)

# Set the task dependencies
etl_task
