from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import os
import logging
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

try:
    # Loading environment variables from .env file
    load_dotenv()
    host = os.getenv("POSTGRES_HOST")
    database = os.getenv("POSTGRES_DB")
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    port = os.getenv("POSTGRES_PORT")

    logger.debug("PostgresSQL connection parameters loaded successfully.")

    postgres_url = f'postgresql://{user}:{password}@{host}:{port}/{database}'
    logger.debug("PostgresSQL connection URL constructed successfully.")

except Exception as error:
    logger.error("Error while connecting to PostgresSQL:", error)

def db_connection():
    return create_engine(postgres_url)

def db_session():
    session = sessionmaker(bind=db_connection())
    session =  session()
    logger.debug("PostgresSQL session created successfully.")
    return session

def close_db_session(session):
    session.close()
    logger.debug("PostgresSQL session closed successfully.")