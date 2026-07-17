import pandas as pd
from src.db import Session, Base, engine
from src.models import Climate
import logging

# Logger do módulo
logger = logging.getLogger(__name__)

# Guardar os dados no banco 
def create_tables(engine) -> None:
    try:
        logger.info("Creating tables")
        Base.metadata.create_all(bind= engine)
        logger.info("Tables created with sucess")
    except Exception as e:
        logger.exception(f"Tables create error: {e}")
        return


def insert_data(data_normalized: pd.Series) -> None:
    with Session() as session:
        try:
            logger.info("Inserting data in database")
            c = Climate(**data_normalized.to_dict())
            session.add(c)
            session.commit()
            logger.info("Data inserted in database with sucess")
        except Exception as e:
            session.rollback()
            logger.exception(f"Error inserting data into the database: {e}")
            return


def load(engine, data_normalized: pd.Series) -> None:
    create_tables(engine)
    insert_data(data_normalized)
