from datetime import datetime
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from .. import schema, models




router = APIRouter()

#get all patients
@router.get("/patients", response_model=List[schema.Patient])
def get_patients(db: Session = Depends(get_db)):
    patients = db.query(models.Patient).all()
    return patients

#Create a new patient
@router.post("/patients", status_code=status.HTTP_201_CREATED, response_model=schema.Patient)
def create_patients(patient: schema.PatientCreate, db: Session = Depends(get_db)):
    patient.birth_date = datetime.strptime(patient.birth_date, '%m-%d-%Y').date()
    new_patient = models.Patient(**patient.dict())
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)

    return new_patient

#get a patient with the given id
@router.get("/patients/{id}", response_model=schema.Patient)
def get_patient(id: int, db: Session = Depends(get_db)):

    patient = db.query(models.Patient).filter(models.Patient.id == id).first()

    if not patient:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"patient with the id: {id} was not found")

    return patient

#get a patient by the first name and last name
@router.get("/patients/", response_model=schema.Patient)
def get_patient(fname: str, lname: str, db: Session = Depends(get_db)):

    patient = db.query(models.Patient).filter(models.Patient.first_name.like(fname), models.Patient.last_name.like(lname)).first()

    if not patient:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"patient with the firstname: {fname}, and lastname: {lname} was not found")

    return patient


#delete a patient with the given id
@router.delete("/patients/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_patient(id: int, db: Session = Depends(get_db)):

    patient = db.query(models.Patient).filter(models.Patient.id == id)
    
    if patient.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"patient with the id: {id} does not exist")

    patient.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


#update a patient with the given id
@router.put("/patients/{id}", response_model=schema.Patient)
def update_patient(id: int, updated_patient: schema.PatientCreate, db: Session = Depends(get_db)):

    patient_query = db.query(models.Patient).filter(models.Patient.id==id)
    
    patient = patient_query.first()

    if patient == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")

    patient_query.update(updated_patient.dict(), synchronize_session=False)
    db.commit()

    return patient_query.first()