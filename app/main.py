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

@app.post("/patients", status_code=status.HTTP_201_CREATED)
def create_patients(patient: Patient, db: Session = Depends(get_db)):
    patient.birth_date = datetime.strptime(patient.birth_date, '%m-%d-%Y').date()
    new_patient = models.Patient(**patient.dict())
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)

    return {"data": new_patient}


@app.get("/patients/{id}")
def get_patient(id: int, db: Session = Depends(get_db)):

    patient = db.query(models.Patient).filter(models.Patient.id == id).first()

    if not patient:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"patient with the id: {id} was not found")

    return {"patient_detail": patient}
