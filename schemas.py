from pydantic import BaseModel
from datetime import date
from typing import Optional

class IndividuBase(BaseModel):
    prenom: Optional[str] = None
    noms: Optional[str] = None
    date_naissance: Optional[date] = None
    date_mort: Optional[date] = None

class IndividuCreate(IndividuBase):
    pass

class Individu(IndividuBase):
    id: int

    class Config:
        orm_mode = True
