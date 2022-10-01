from tkinter import image_names
from typing import List
from fastapi import Response, status, HTTPException, Depends, File, UploadFile, Form, APIRouter
from sqlalchemy.orm import Session
from .. import models, schema
from ..database import get_db
import secrets
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from PIL import Image


router = APIRouter(
    prefix="/acquisitions",
    tags= ['Acquisitions']

)

router.mount("/static", StaticFiles(directory="static"), name="static")

#Add a new acquisition for a patient
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.Acquisition)
async def create_acquisition(file: UploadFile = File(), eye: str = Form(), site_name: str = Form(), date_taken: str = Form(), operator_name: str = Form(), patient_id: int = Form(), db: Session = Depends(get_db)):
    
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

    new_acquisition = models.Acquisition(eye=eye, site_name=site_name, date_taken=date_taken, operator_name= operator_name, image_data = token_name, patient_id = patient_id)
    db.add(new_acquisition)
    db.commit()
    db.refresh(new_acquisition)

    return new_acquisition


#List all patient acquisitions (by patient id) 
@router.get("/{id}", response_model=List[schema.Allacquisition])
def get_acquisitions(id: int, db: Session = Depends(get_db)):
    acquisitions = db.query(models.Acquisition).filter(models.Acquisition.patient_id == id).all()
    return acquisitions

#delete an acquisition with the given id
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_acquisition(id: int, db: Session = Depends(get_db)):

    acquisition = db.query(models.Acquisition).filter(models.Acquisition.id == id)

    
    
    if acquisition.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"acquisition with the id: {id} does not exist")

    acquisition.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


#download an image (by acquisition id)
@router.get("/download/{id}")
def download_acquisition_image(id: int, db: Session = Depends(get_db)):

    FILEPATH = "./static/images/"
    acquisition_row = db.query(models.Acquisition).filter(models.Acquisition.id == id).first()
    image_name = vars(acquisition_row)["image_data"]

    image_path = FILEPATH + image_name
    return FileResponse(path=image_path, filename=image_path)