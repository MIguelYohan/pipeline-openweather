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


def local_data_normalize(data: dict) -> pd.Series:
    return pd.Series({"Local": data["name"]}, name= "local")


def weather_data_normalize(data: dict) -> pd.Series:
    weather_data = pd.Series(data["weather"][0], name= "weather_data")
    weather_data = weather_data.drop(["id", "icon"])
    weather_data = weather_data.rename({"main": "condition"})
    return weather_data


def temperature_data_normalize(data: dict) -> pd.Series:
    temperature_data = pd.Series(data["main"], name= "temperature_data")
    temperature_data = temperature_data.drop(["pressure", "humidity", "sea_level", "grnd_level"], errors="ignore")
    temperature_data = temperature_data.rename({"temp": "temperature"})
    return temperature_data


def wind_data_normalize(data: dict) -> pd.Series:
    wind_data = pd.Series(data["wind"], name= "wind_data")
    wind_data = wind_data.rename({"speed": "wind_speed", "deg": "wind_direction", "gust": "wind_gust_speed"})
    return wind_data


def clouds_data_normalize(data: dict) -> pd.Series: 
    clouds_data = pd.Series(data["clouds"], name= "clouds_data")
    clouds_data = clouds_data.rename({"all": "clouds"})
    return clouds_data


def normalize_all(data: dict) -> list[pd.Series]:
    return [
        local_data_normalize(data),
        weather_data_normalize(data),
        temperature_data_normalize(data),
        wind_data_normalize(data),
        clouds_data_normalize(data)
    ]


def concat_all_data(data_normalized: pd.Series) -> pd.DataFrame:
    all_data = pd.concat(data_normalized)
    return pd.Series(all_data)


def get_data():
    with open(get_latest_file(), 'r', encoding= 'utf-8') as file:
        return json.load(file)


if __name__ == '__main__':
    data = get_data()
    data_normalized = normalize_all(data)
    print(concat_all_data(data_normalized))
