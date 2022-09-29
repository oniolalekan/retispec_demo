from datetime import datetime
from multiprocessing import synchronize
from fastapi import FastAPI, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session
from . import models, schema
from .database import engine, get_db


#this handles the migration. Create the tables from the python models using alchemy ORM
models.Base.metadata.create_all(bind=engine)

app = FastAPI()




@app.get("/patients")
def get_patients(db: Session = Depends(get_db)):
    patients = db.query(models.Patient).all()
    return {"data": patients}

@app.post("/patients", status_code=status.HTTP_201_CREATED)
def create_patients(patient: schema.Patient, db: Session = Depends(get_db)):
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


@app.delete("/patients/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_patient(id: int, db: Session = Depends(get_db)):

    patient = db.query(models.Patient).filter(models.Patient.id == id)
    
    if patient.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"patient with the id: {id} does not exist")

    patient.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/patients/{id}")
def update_patient(id: int, updated_patient: schema.Patient, db: Session = Depends(get_db)):

    patient_query = db.query(models.Patient).filter(models.Patient.id==id)
    
    patient = patient_query.first()

    if patient == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")

    patient_query.update(updated_patient.dict(), synchronize_session=False)
    db.commit()

    return {"data": patient_query.first()}