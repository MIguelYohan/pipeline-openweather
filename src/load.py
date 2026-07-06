import pandas as pd
from db import Session, Base, engine
from models import Climate
from transform import get_data, normalize_all, concat_all_data, export_processed
# Guardar os dados no banco 

def create_tables(engine) -> None:
    Base.metadata.create_all(bind= engine)


def insert_data(data_normalized: pd.Series) -> None:
    with Session() as session:
        try:
            c = Climate(**data_normalized.to_dict())
            session.add(c)
            session.commit()
        except Exception as e:
            session.rollback()
            print("Error inserting data into the database")
            raise


if __name__ == '__main__':
    r_data = get_data()
    n_data = normalize_all(r_data)
    data = concat_all_data(n_data)
    try:
        create_tables(engine)
        print("Tabelas criadas/verificadas com sucesso.")
    except Exception as e:
        print(f"Erro ao criar as tabelas: {e}")

    try:
        insert_data(data)
        export_processed(data)
    except Exception as e:
        print(f"Erro ao inserir os dados: {e}")