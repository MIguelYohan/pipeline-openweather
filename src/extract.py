import json
import requests
import logging
import sys

# Logger desse módulo
logger = logging.getLogger(__name__)

def extract(url, output_path) -> None:
    logger.info("Connecting with API...")
    try:
        response = requests.get(url= url, timeout= 10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.exception(f"Connection with API error: {e}")
        sys.exit(1)
    
    data = response.json()
    logger.info(f"API response received: status {response.status_code}")

    try:
        output_path.parent.mkdir(parents= True, exist_ok= True) # Garante que a pasta destino exista
        with open(output_path, "w", encoding= 'utf-8') as file:
            json.dump(data, file, indent= 4)
        logger.info("Raw data saved in data/raw")
    except Exception as e:
        logger.exception(f"Raw file save error: {e}")
        sys.exit(1)
