from sqlalchemy import Column, Integer, String
#from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from .database import Base

#SQLAlchemy model Patient: Responsible for defining the columns 
#of our "pateint" table within the RDS used. It's agnostic to the choice of RDBMS.
class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, nullable=False)
    last_name = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    birth_date = Column(String, nullable=False)
    sex = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))