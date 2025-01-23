# Start with a Python base image
FROM python:3.9

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Apache Airflow
RUN pip install apache-airflow[postgres,celery]==2.9.0

# Set the Airflow home directory
ENV AIRFLOW_HOME=/opt/airflow

# Set the working directory
WORKDIR /opt/airflow

# Copy DAGs and dependencies
COPY dags/ /opt/airflow/dags/
COPY requirements.txt /opt/airflow/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r /opt/airflow/requirements.txt

# Expose Airflow webserver port
EXPOSE 8080

# Default command
CMD ["airflow", "webserver"]
