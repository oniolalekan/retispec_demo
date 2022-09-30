from typing import List
from fastapi import Response, status, HTTPException, Depends, File, UploadFile, Form, APIRouter
from sqlalchemy.orm import Session
from .. import models, schema
from ..database import get_db
import secrets
from fastapi.staticfiles import StaticFiles
from PIL import Image


router = APIRouter()

router.mount("/static", StaticFiles(directory="static"), name="static")

#Create a new acquisition
@router.post("/acquisitions", status_code=status.HTTP_201_CREATED, response_model=schema.Acquisition)
async def create_acquisition(file: UploadFile = File(), eye: str = Form(), site_name: str = Form(), date_taken: str = Form(), operator_name: str = Form(), db: Session = Depends(get_db)):
    
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


#get all acquisitions
@router.get("/acquisitions", response_model=List[schema.Allacquisition])
def get_acquisitions(db: Session = Depends(get_db)):
    acquisitions = db.query(models.Acquisition).all()
    return acquisitions

#delete an acquisition with the given id
@router.delete("/acquisitions/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_acquisition(id: int, db: Session = Depends(get_db)):

    acquisition = db.query(models.Acquisition).filter(models.Acquisition.id == id)
    
    if acquisition.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"acquisition with the id: {id} does not exist")

    acquisition.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)