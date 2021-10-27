#Python
from typing import List, Optional

#Pydantic
from pydantic import BaseModel

#FastApi
from fastapi import FastAPI
from fastapi import Body

# esta variable contiene a toda nuestra aplicacion, FastAPI es una instancia por los ()
app = FastAPI() 

# Models

class Person(BaseModel):
    first_name: str
    last_name: str
    age: int
    hair_color: Optional[str] = None
    is_married: Optional[bool] = None

@app.get("/")  #el get es Path 
def home():
     # para comunicarse se hace mediante Json y en py el Json es un dicci {}
    return {"hello": "world"}   

 # Request and response body
  
 # aca usamos post porque le pedimos al sevidor datos si enviamos seria get
 #dentro de create_person definimos persona con la Person y lo igualamos a body que se importa para poner los ... que dicen que es obligatiro el parametro
@app.post("/person/new")
 
def create_person(person: Person = Body(...)):
    return person
