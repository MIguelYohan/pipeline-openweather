from pathlib import Path
from datetime import datetime
import pandas as pd
import json
import logging

# Logger desse módulo
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).parent.parent
GET_FROM = BASE_DIR / "data" / "raw"

def get_latest_file() -> Path:
    logger.info("Scanning data/raw directory...")
    files = list(GET_FROM.glob("extract_data_*.json")) # Itera sobre todos os arquivos da pasta raw
    if not files:
        logger.error("No source in data/raw directory")
        return
    return max(files, key=lambda x: x.stat().st_mtime) # Retorna o maximo em relação ao modification time nos metadados do arquivo

def get_data() -> dict:
    logger.info("Fetching data from raw directory")
    with open(get_latest_file(), 'r', encoding= 'utf-8') as file:
        return json.load(file)


def local_data_normalize(data: dict) -> pd.Series:
    logger.info("Local data normalized with success")
    return pd.Series({"local": data["name"]}, name= "local")


def weather_data_normalize(data: dict) -> pd.Series:
    weather_data = pd.Series(data["weather"][0], name= "weather_data")
    weather_data = weather_data.drop(["id", "icon"], errors= "ignore")
    weather_data = weather_data.rename({"main": "condition"})
    logger.info("Weather data normalized with success")
    return weather_data


def temperature_data_normalize(data: dict) -> pd.Series:
    temperature_data = pd.Series(data["main"], name= "temperature_data")
    temperature_data = temperature_data.drop(["pressure", "humidity", "sea_level", "grnd_level"], errors="ignore")
    temperature_data = temperature_data.rename({"temp": "temperature"})
    logger.info("Temperature data normalized with success")
    return temperature_data


def wind_data_normalize(data: dict) -> pd.Series:
    wind_data = pd.Series(data["wind"], name= "wind_data")
    wind_data = wind_data.rename({"speed": "wind_speed", "deg": "wind_direction", "gust": "wind_gust_speed"})
    logger.info("Wind data normalized with success")
    return wind_data


def clouds_data_normalize(data: dict) -> pd.Series: 
    clouds_data = pd.Series(data["clouds"], name= "clouds_data")
    clouds_data = clouds_data.rename({"all": "clouds"})
    logger.info("Clouds data normalized with success")
    return clouds_data


def normalize_all(data: dict) -> list[pd.Series]:
    logger.info("Normalizing data...")
    return [
        local_data_normalize(data),
        weather_data_normalize(data),
        temperature_data_normalize(data),
        wind_data_normalize(data),
        clouds_data_normalize(data)
    ]


def concat_all_data(data_normalized: list[pd.Series]) -> pd.Series:
    logger.info("All data normalize with success")
    return pd.concat(data_normalized)
    

def export_processed(all_data: pd.Series) -> None:
    EXPORT_TO = Path(__file__).parent.parent / "data" / "processed"
    EXPORT_TO.mkdir(parents=True, exist_ok=True)
    CREATED_FILE = EXPORT_TO / f"processed_data_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
    try:
        logger.info("Saving normalized data in data/processed")
        json_data = all_data.to_dict()
        with open(CREATED_FILE, 'w', encoding='utf-8') as file:
            json.dump(json_data, file, indent= 4)
            logger.info("Processed data saved in data/processed")
    except Exception as e:
        logger.exception(f"Process file save error: {e}")
        return


def transform() -> pd.Series:
    r_data = get_data()
    n_data = normalize_all(r_data)
    processed = concat_all_data(n_data)
    export_processed(processed)
    return processed


if __name__ == '__main__':
    raw_data = get_data()
    data_normalized = normalize_all(raw_data)
    processed = concat_all_data(data_normalized)
    print(processed)
    export_processed(processed)
