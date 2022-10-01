from pydantic import BaseModel
from typing import List

#Pydantic model: Patient: defines the structure of the request and response.
#a form of validation to ensure all the fields are completed.
class PatientBase(BaseModel):
    last_name: str
    first_name:str
    birth_date: str
    sex: str

class PatientCreate(PatientBase):
    pass

class Patient(PatientBase):
    
    class Config:
        orm_mode = True


class Acquisition(BaseModel):
    eye: str
    site_name:str
    date_taken: str
    operator_name: str
    image_data: str
    patient: Patient

    class Config:
        orm_mode = True


class Allacquisition(BaseModel):
    eye: str
    site_name:str
    date_taken: str
    operator_name: str
    patient: Patient

    class Config:
        orm_mode = True