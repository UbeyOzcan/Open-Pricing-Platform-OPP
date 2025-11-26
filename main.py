import psycopg
import json
import pandas as pd
import time

start = time.time()

with open('auth.json', 'r') as file:
    auth = json.load(file)

# Fetch variables
USER = auth["user"]
PASSWORD = auth["password"]
HOST = auth["host"]
PORT = auth["port"]
DBNAME = auth["database"]

# Connect to the database
try:
    connection = psycopg.connect(
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT,
        dbname=DBNAME
    )
    print("Connection successful!")

    # Create a cursor to execute SQL queries
    cur = connection.cursor()
    cur.execute(f"SELECT * FROM frenchmtpl")
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    df = pd.DataFrame(rows, columns=columns)
    print(df.head(1))
    cur.close()
    connection.close()
    end = time.time()
    print(f"Total runtime of the program is {round(end - start, 2)} seconds")
except Exception as e:
    print(f"Failed to connect: {e}")