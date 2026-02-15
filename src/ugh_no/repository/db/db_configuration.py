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
            logger.debug("PostgresSQL connection URL constructed successfully.")
        except Exception as error:
            logger.error("Error while connecting to PostgresSQL:", error)

    def db_connection(self):
        if self.postgres_url is None:
            self.get_url_connection()
        return create_engine(self.postgres_url)

    def db_session(self):
        session = sessionmaker(bind=self.db_connection())
        session =  session()
        logger.debug("PostgresSQL session created successfully.")
        return session