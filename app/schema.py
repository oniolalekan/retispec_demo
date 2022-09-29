from pydantic import BaseModel

#Pydantic model: Patient: defines the structure of the request and response.
#a form of validation to ensure all the fields are completed.
class Patient(BaseModel):
    last_name: str
    first_name:str
    birth_date: str
    sex: str