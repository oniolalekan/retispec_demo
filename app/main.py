from datetime import datetime
from fastapi import FastAPI, status, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db


#this handles the migration. Create the tables from the python models using alchemy ORM
models.Base.metadata.create_all(bind=engine)

app = FastAPI()




class Patient(BaseModel):
    last_name: str
    first_name:str
    birth_date: str


@app.get("/patients")
def get_patients(db: Session = Depends(get_db)):
    patients = db.query(models.Patient).all()
    return {"data": patients}

