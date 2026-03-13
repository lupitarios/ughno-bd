from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import os
import logging
from dotenv import load_dotenv

logger = logging.getLogger(__name__)


def close_db_session(session):
    session.close()
    logger.debug("PostgresSQL session closed successfully.")


class DBConfiguration:

    instance = None

    def __init__(self):
        self. postgres_url = None
        self.get_url_connection()

    '''Singleton pattern implementation to ensure only one instance of DBConfiguration exists.'''
    def __new__(cls):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def get_url_connection(self):
        try:
            # Loading environment variables from .env file
            load_dotenv()
            host = os.getenv("POSTGRES_HOST")
            database = os.getenv("POSTGRES_DB")
            user = os.getenv("POSTGRES_USER")
            password = os.getenv("POSTGRES_PASSWORD")
            port = os.getenv("POSTGRES_PORT")

            logger.debug("PostgresSQL connection parameters loaded successfully.")

            self.postgres_url = f'postgresql://{user}:{password}@{host}:{port}/{database}'
            logger.info(f"PostgresSQL connection URL constructed successfully -> {self.postgres_url}")
        except Exception as error:
            logger.error(f"Error while connecting to PostgresSQL:{error}")

    def create_engine(self):
        try:
            if self.postgres_url is None:
                self.get_url_connection()
            return create_engine(
                self.postgres_url,
                pool_size=10,
                max_overflow=20,
                pool_timeout=30,)
        except Exception as error:
            logger.error(f"Error while connecting to PostgresSQL:{error}" )

    def get_db_session(self):
        try:
            session = sessionmaker(bind=self.create_engine(), autocommit=False, autoflush=False)
            session =  session()
            logger.debug("PostgresSQL session created successfully.")
            return session
        except Exception as error:
            logger.error(f"Error while creating PostgresSQL session:{error}")