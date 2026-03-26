import os
from dotenv import load_dotenv
import psycopg


load_dotenv()


def get_connection():
    """
    Create and return a PostgreSQL connection using environment variables.
    """
    conn = psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )
    return conn