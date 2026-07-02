import json
from datetime import datetime
import requests
import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
timestamp = datetime.now().strftime("%Y%m%d_%H%M") # Horario atual da geração do arquivo
output_path = BASE_DIR / "data" / "raw" / f"extract_data_{timestamp}.json" # Caminho até a pasta raw

load_dotenv()
# Chave da API
API_KEY = os.getenv("API_KEY")
# Latitude e Longitude para extração dos dados de Brasília-DF
lat = -15.7942 
lon = -47.8822

url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric&lang=pt_br"
response = requests.get(url= url)
data = response.json()

if response.status_code != 200:
    print(f"Erro na requisição: {response.status_code} - {data.get('message')}")
else:
    output_path.parent.mkdir(parents= True, exist_ok= True) # Garante que a pasta destino exista
    with open(output_path, "w", encoding= 'utf-8') as file:
        json.dump(data, file, indent= 4)
