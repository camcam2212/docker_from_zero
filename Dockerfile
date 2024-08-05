FROM apache/airflow:2.9.3

USER root

RUN apt-get update && apt-get install -y \
    libpq-dev \
    build-essential
# Đảm bảo thư mục CSV tồn tại trong image
RUN mkdir -p /opt/airflow/csv

USER airflow

COPY requirements.txt .
RUN pip install -r requirements.txt
