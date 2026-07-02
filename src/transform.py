import pandas as pd
import json
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
GET_FROM = BASE_DIR / "data" / "raw"

def get_latest_file():
    files = list(GET_FROM.glob("extract_data_*.json")) # Itera sobre todos os arquivos da pasta raw
    if not files:
         raise FileNotFoundError("Nenhum arquivo encontrado no diretório data/raw")
    return max(files, key=lambda x: x.stat().st_mtime) # Retorna o maximo em relação ao modification time nos metadados do arquivo

with open(get_latest_file(), 'r', encoding= 'utf-8') as file:
    data = json.load(file)

# == Tratamento de Nomes / Retirando valores inuteis ==
# Transformar isso em diferentes funcoes:
local = pd.Series({"local": data["name"]}, name= "local") # Local no mapa da extração dos dados
weather_data = pd.Series(data["weather"][0], name= "weather_data").drop(["id", "icon"]).rename({"main": "condition"}) # Pega a condicao de tempo primaria
temperature_data = pd.Series(data["main"], name= "temperature_data").drop(["pressure", "humidity", "sea_level", "grnd_level"], errors="ignore").rename({"temp": "temperature"})
wind_data = pd.Series(data["wind"], name= "wind_data").rename({"speed": "wind_speed", "deg": "wind_direction", "gust": "wind_gust_speed"})
clouds = pd.Series(data["clouds"], name= "clouds_data").rename({"all": "clouds"})

all_data = pd.concat(
    [local, weather_data, temperature_data, wind_data, clouds])
