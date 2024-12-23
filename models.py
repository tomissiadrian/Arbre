from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Individu(Base):
    __tablename__ = "individus"
    
    id = Column(Integer, primary_key=True, index=True)
    prenom = Column(String, nullable=False)
    noms = Column(String, nullable=False)
    date_naissance = Column(Date, nullable=False)
    date_mort = Column(Date, nullable=True)

class Relation(Base):
    __tablename__ = "relations"
    
    id = Column(Integer, primary_key=True, index=True)
    parent_id = Column(Integer, ForeignKey("individus.id"), nullable=False)
    enfant_id = Column(Integer, ForeignKey("individus.id"), nullable=False)
