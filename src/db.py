# Conexão do MySQL com o SqlAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import logging
import os
import sys

# Logger desse módulo
logger = logging.getLogger(__name__)

load_dotenv()
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_USER_PASSWORD = os.getenv("DB_USER_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

url = f"mysql+mysqldb://{DB_USER}:{DB_USER_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
try:
    logger.info("Connecting with MySQL Database...")
    engine = create_engine(url=url) # Inicia a conexão do banco de dados com o Python
except Exception as e:
    logger.exception(f"Error with the database connection: {e}")
    sys.exit(1)

Session = sessionmaker(bind=engine) # Usado para fazer modificações no banco
Base = declarative_base() # Classe para criar as tabelas do banco pela ORM do SqlAlchemy
