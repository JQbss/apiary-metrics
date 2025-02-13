import psycopg2
conn = psycopg2.connect(
    dbname="apiary_metrics",
    user="postgres",  # Try with superuser first
    password="admin",
    host="localhost",
    port="5432"
)