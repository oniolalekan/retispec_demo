from fastapi import FastAPI
from . import models
from .routers import patient, acquisition
from .database import engine


#this handles the migration. Create the tables from the python models using alchemy ORM
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(patient.router)
app.include_router(acquisition .router)











