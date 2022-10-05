from fastapi import FastAPI
from . import models
from .routers import patient, acquisition
from .database import engine
from fastapi.middleware.cors import CORSMiddleware


#this handles the migration. Create the tables from the python models using alchemy ORM
models.Base.metadata.create_all(bind=engine)

app = FastAPI()



origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(patient.router)
app.include_router(acquisition.router)











