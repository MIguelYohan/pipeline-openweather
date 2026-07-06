# Conexão do MySQL com o SqlAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_USER_PASSWORD = os.getenv("DB_USER_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

url = f"mysql+mysqldb://{DB_USER}:{DB_USER_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(url=url) # Inicia a conexão do banco de dados com o Python
Session = sessionmaker(bind=engine) # Usado para fazer modificações no banco
Base = declarative_base() # Classe para criar as tabelas do banco pela ORM do SqlAlchemy