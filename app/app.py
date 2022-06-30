import logging

import pandas as pd
import requests
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

db_name = 'postgres'
db_user = 'postgres'
db_pass = 'postgrespw'
db_host = 'host.docker.internal'
db_port = '49154'

db_log_file_name = 'logs.txt'
db_handler_log_level = logging.INFO
db_logger_log_level = logging.DEBUG

db_handler = logging.FileHandler(db_log_file_name)
db_handler.setLevel(db_handler_log_level)

db_logger = logging.getLogger('sqlalchemy')
db_logger.addHandler(db_handler)
db_logger.setLevel(db_logger_log_level)

db_string = 'postgresql://{}:{}@{}:{}/{}'.format(db_user,
                                                 db_pass,
                                                 db_host,
                                                 db_port,
                                                 db_name)
engine = create_engine(db_string)
Base = declarative_base()

Session = sessionmaker(bind=engine)

base_url = "https://www.ebi.ac.uk/pdbe/graph-api/compound/summary/"
chemical_compounds = ['ADP', 'ATP', 'STI', 'ZID', 'DPM', 'XP9', '18W', '29P']


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

    response = requests.get(base_url + comp)
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

    class Compound(Base):
        __tablename__ = "compounds"
        id = Column(Integer, primary_key=True)
        name = Column(String())
        compound = Column(String())
        formula = Column(String())
        inchi = Column(String())
        inchi_key = Column(String())
        smiles = Column(String())
        cross_links_count = Column(Integer)

        def __str__(self):
            return self.compound

    Base.metadata.create_all(engine)

    try:
        with Session() as session:
            for comp in chemical_compounds:
                result = pull_data(comp)
                name = result[comp][0]['name']
                compound = list(result.keys())[0]
                formula = result[comp][0]['formula']
                inchi = result[comp][0]['inchi']
                inchi_key = result[comp][0]['inchi_key']
                smiles = result[comp][0]['smiles']
                cross_links_count = len(result[comp][0]['cross_links'])
                session.add(Compound(
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
        df = pd.read_sql_table(table_name=table_name, con=engine)
    except ValueError as e:
        print(e)
    else:
        df.iloc[:, 1:7] = (df.iloc[:, 1:7].astype(str).
                           applymap(lambda x: x if len(x) < 13 else x[:10] + '...'))
        pd.set_option('display.expand_frame_repr', False)
        print(df.to_string(index=False))


if __name__ == "__main__":
    post_data(chemical_compounds)
    print_table("compounds")
