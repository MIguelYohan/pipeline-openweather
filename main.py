import os
from dotenv import load_dotenv
from datetime import datetime
from pathlib import Path
from src.logconfig import setup_logging
from src.extract import extract
from src.transform import transform
from src.load import load
from src.db import engine

BASE_DIR = Path(__file__).resolve().parent # Raiz do projeto
timestamp = datetime.now().strftime("%Y%m%d_%H%M") # Horario atual da geração do arquivo
output_path = BASE_DIR / "data" / "raw" / f"extract_data_{timestamp}.json" # Caminho até a pasta raw

# Latitude e longitude de Brasília - DF
lat = -15.7942 
lon = -47.8822

load_dotenv()
API_KEY = os.getenv("API_KEY")

url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric&lang=pt_br"


if __name__ == '__main__':
    setup_logging() # Configuraçoes de logging
    # Execução da pipeline
    extract(url, output_path)
    data_processed = transform()
    load(engine, data_processed)
    