import os
import psycopg2 # Use psycopg2 for PostgreSQL instead of pymssql
from dotenv import load_dotenv

 # Load environment variables from .env file
load_dotenv()

# Fetch the database connection string from an environment variable
dbhost = os.getenv("DBHOST")
dbuser = os.getenv("DBUSER")
dbpassword = os.getenv("DBPASSWORD")
dbname = os.getenv("DBNAME")
dbport = os.getenv("DBPORT")


conn = psycopg2.connect(host=dbhost, port=dbport, user=dbuser, password=dbpassword, dbname=dbname)   
cursor = conn.cursor() 
cursor.execute("UPDATE devices SET inuse = FALSE")
conn.commit()
conn.close()