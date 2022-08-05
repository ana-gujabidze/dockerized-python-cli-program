import logging
import os

import pandas as pd
import requests
from dotenv import load_dotenv
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql import exists

from storage import database, models

BASE_URL = "https://www.ebi.ac.uk/pdbe/graph-api/compound/summary/"
CHEMICAL_COMPOUNDS = ['ADP', 'ATP', 'STI', 'ZID', 'DPM', 'XP9', '18W', '29P']

# Start of logging
db_log_file_name = 'console.log'
db_handler_log_level = logging.INFO
db_logger_log_level = logging.DEBUG

db_handler = logging.FileHandler(db_log_file_name)
db_handler.setLevel(db_handler_log_level)

db_logger = logging.getLogger('sqlalchemy')
db_logger.addHandler(db_handler)
db_logger.setLevel(db_logger_log_level)
# End of logging


def pull_data(comp):
    '''
    Get data out of API ebi-ac-uk.

    This function simply gets data about compound from API ebi-ac-uk
    and returns data in JSON format.

    Parameters
    ----------
    comp : str
        Single compound.
    '''

    response = requests.get(BASE_URL + comp)
    result = response.json()
    return result


def post_data(chemical_compounds):
    '''
    Store data from API ebi-ac-uk in PostgreSQL database.

    This function simply posts data about compound from API ebi-ac-uk
    into PostgreSQL database.

    Parameters
    ----------
    chemical_compounds : list of str
        Multiple compounds.
    '''

    database.Base.metadata.create_all(database.engine)

    try:
        with database.Session() as session:
            for comp in chemical_compounds:
                comp_exists = session.query(exists().where(models.Compound.compound == comp)).scalar()
                if not comp_exists:
                    result = pull_data(comp)
                    name = result[comp][0]['name']
                    compound = list(result.keys())[0]
                    formula = result[comp][0]['formula']
                    inchi = result[comp][0]['inchi']
                    inchi_key = result[comp][0]['inchi_key']
                    smiles = result[comp][0]['smiles']
                    cross_links_count = len(result[comp][0]['cross_links'])
                    session.add(models.Compound(
                        name=name,
                        compound=compound,
                        formula=formula,
                        inchi=inchi,
                        inchi_key=inchi_key,
                        smiles=smiles,
                        cross_links_count=cross_links_count
                    ))
            session.commit()
    except KeyError as e:
        print(e)
    except requests.exceptions.JSONDecodeError as e:
        print(e)


def print_table(table_name):
    '''
    Print PostgreSQL database content into CLI.

    This function simply prints out PostgreSQL database content.
    If any column content is longer than 13 characters, text gets
    truncated.

    Parameters
    ----------
    table_name : str
        Name of PostgreSQL table.
    '''
    try:
        df = pd.read_sql_table(table_name=table_name, con=database.engine)
    except ValueError as e:
        print(e)
    else:
        df.iloc[:, 1:7] = (df.iloc[:, 1:7].astype(str).
                           applymap(lambda x: x if len(x) < 13 else x[:10] + '...'))
        pd.set_option('display.expand_frame_repr', False)
        print(df.to_string(index=False))


if __name__ == "__main__":
    post_data(CHEMICAL_COMPOUNDS)
    print_table("compounds")
