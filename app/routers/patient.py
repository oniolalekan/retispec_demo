from datetime import date, datetime
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
#from app.models import Patient
from .. import schema, models




router = APIRouter(
    prefix="/patients",
    tags=['Patients']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.Patient)
def create_patient(lname: str, fname: str, bdate: date, sex: str, db: Session = Depends(get_db)):
    
    new_patient = models.Patient(last_name=lname, first_name=fname, birth_date=bdate, sex=sex)
        
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)

    return new_patient


@router.get("/{id}", response_model=schema.Patient)
def get_patient(id: int, db: Session = Depends(get_db)):

    patient = db.query(models.Patient).filter(models.Patient.id == id).first()

    if not patient:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"patient with the id: {id} was not found")

    return patient

#get a patient by the first name and last name
@router.get("/{first_name}/{last_name}", response_model=schema.Patient)
def get_patient(fname: Optional[str] = "", lname: Optional[str] = "", db: Session = Depends(get_db)):

    patient = db.query(models.Patient).filter(models.Patient.first_name.contains(fname), models.Patient.last_name.contains(lname)).first()

    if not patient:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"patient with the firstname: {fname}, and lastname: {lname} was not found")

    return patient


#delete a patient with the given id
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_patient(id: int, db: Session = Depends(get_db)):

    patient = db.query(models.Patient).filter(models.Patient.id == id)
    
    if patient.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"patient with the id: {id} does not exist")

    patient.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


#update a patient with the given id
@router.put("/{id}", response_model=schema.Patient)
def update_patient(id: int, updated_patient: schema.PatientCreate, db: Session = Depends(get_db)):

    patient_query = db.query(models.Patient).filter(models.Patient.id==id)
    
    patient = patient_query.first()

    if patient == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")

    patient_query.update(updated_patient.dict(), synchronize_session=False)
    db.commit()

    return patient_query.first()