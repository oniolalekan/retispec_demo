from datetime import datetime
from multiprocessing import synchronize
from typing import List
from fastapi import FastAPI, Response, status, HTTPException, Depends, File, UploadFile, Form
from sqlalchemy.orm import Session
from . import models, schema
from .database import engine, get_db
import secrets
from fastapi.staticfiles import StaticFiles
from PIL import Image


#this handles the migration. Create the tables from the python models using alchemy ORM
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


#get all patients
@app.get("/patients", response_model=List[schema.Patient])
def get_patients(db: Session = Depends(get_db)):
    patients = db.query(models.Patient).all()
    return patients

#Create a new patient
@app.post("/patients", status_code=status.HTTP_201_CREATED, response_model=schema.Patient)
def create_patients(patient: schema.PatientCreate, db: Session = Depends(get_db)):
    patient.birth_date = datetime.strptime(patient.birth_date, '%m-%d-%Y').date()
    new_patient = models.Patient(**patient.dict())
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)

    return new_patient

#get a patient with the given id
@app.get("/patients/{id}", response_model=schema.Patient)
def get_patient(id: int, db: Session = Depends(get_db)):

    patient = db.query(models.Patient).filter(models.Patient.id == id).first()

    if not patient:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"patient with the id: {id} was not found")

    return patient

#get a patient by the first name and last name
@app.get("/patients/", response_model=schema.Patient)
def get_patient(fname: str, lname: str, db: Session = Depends(get_db)):

    patient = db.query(models.Patient).filter(models.Patient.first_name.like(fname), models.Patient.last_name.like(lname)).first()

    if not patient:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"patient with the firstname: {fname}, and lastname: {lname} was not found")

    return patient


#delete a patient with the given id
@app.delete("/patients/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_patient(id: int, db: Session = Depends(get_db)):

    patient = db.query(models.Patient).filter(models.Patient.id == id)
    
    if patient.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"patient with the id: {id} does not exist")

    patient.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


#update a patient with the given id
@app.put("/patients/{id}", response_model=schema.Patient)
def update_patient(id: int, updated_patient: schema.PatientCreate, db: Session = Depends(get_db)):

    patient_query = db.query(models.Patient).filter(models.Patient.id==id)
    
    patient = patient_query.first()

    if patient == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")

    patient_query.update(updated_patient.dict(), synchronize_session=False)
    db.commit()

    return patient_query.first()


#Create a new acquisition
@app.post("/acquisitions", status_code=status.HTTP_201_CREATED, response_model=schema.Acquisition)
async def create_file(file: UploadFile = File(), eye: str = Form(), site_name: str = Form(), date_taken: str = Form(), operator_name: str = Form(), db: Session = Depends(get_db)):
    
    FILEPATH = "./static/images/"
    filename = file.filename
    extension = filename.split(".")[1]

    if extension not in ["png", "jpg"]:
        return {"status": "error", "detail": "File extension not allowed"}

    token_name = secrets.token_hex(10) + "." + extension
    generated_name = FILEPATH + token_name
    file_content = await file.read()

    with open(generated_name, "wb") as file:
        file.write(file_content)

    #PILLOW
    print(generated_name)
    img = Image.open(generated_name)
    img = img.resize(size = (200, 200))
    img.save(generated_name)

    new_acquisition = models.Acquisition(eye=eye, site_name=site_name, date_taken=date_taken, operator_name= operator_name, image_data = token_name)
    db.add(new_acquisition)
    db.commit()
    db.refresh(new_acquisition)

    return new_acquisition


#get all patients
@app.get("/acquisitions", response_model=List[schema.Allacquisition])
def get_acquisitions(db: Session = Depends(get_db)):
    acquisitions = db.query(models.Acquisition).all()
    return acquisitions



