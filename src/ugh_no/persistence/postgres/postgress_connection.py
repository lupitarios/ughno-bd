import psycopg2
import os
from dotenv import load_dotenv, dotenv_values
from pathlib import Path

def postgres_connection():
    connection = None
    cursor = None

    try:
        # Loading environment variables from .env file
        load_dotenv()

        print(f" ENV HOST-> {os.getenv("POSTGRES_HOST")}")
        connection = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST"),
            database=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            port=os.getenv("POSTGRES_PORT")
        )
        print("Connection to PostgresSQL database established successfully.")

        cursor = connection.cursor()
        print("PostgresSQL connection established successfully.")
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()
        print("PostgresSQL database version:", db_version)
        print(connection.get_dsn_parameters(), "\n")

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while connecting to PostgresSQL:", error)
    finally:
        if cursor is not None:
            try:
                cursor.close()
            except (Exception, psycopg2.DatabaseError) as error:
                print("Error while closing cursor:", error)

        if connection is not None:
            try:
                connection.close()
            except (Exception, psycopg2.DatabaseError) as error:
                print("Error while closing connection:", error)

            print("PostgresSQL connection closed.")

if __name__ == '__main__':
    postgres_connection()