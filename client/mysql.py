import mysql.connector
import os
from functools import lru_cache

# Function to get the MySQL connection
@lru_cache(maxsize=4)
def get_mysql_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),         # Your MySQL host
        user=os.getenv("DB_USER"),              # Your MySQL user
        password=os.getenv("DB_PASSWORD"),      # Your MySQL password
        database=os.getenv("DB_DATABASE_WALLET")
    )
