from sqlalchemy import Column, Integer, String

from .database import Base


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
