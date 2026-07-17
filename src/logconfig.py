from pathlib import Path
import logging
import sys

BASE_DIR = Path(__file__).resolve().parents[1] # Raiz do projeto

def setup_logging():
    log_path = BASE_DIR / "logs" / "pipeline-etl.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)

    # Configurando sistema de logs com logging
    sys.stdout.reconfigure(encoding="utf-8")  # Previni que os logs causem erros de unicode
    logging.basicConfig(
        level= logging.INFO,
        format="%(asctime)s | %(name)s - %(levelname)s → %(message)s",
        handlers=[
            logging.FileHandler(log_path, encoding="utf-8"),
            logging.StreamHandler()
        ]
    )