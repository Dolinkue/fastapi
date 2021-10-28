#Python
from typing import List, Optional

#Pydantic
from pydantic import BaseModel

#FastApi
from fastapi import FastAPI
from fastapi import Body, Query, Path

# esta variable contiene a toda nuestra aplicacion, FastAPI es una instancia por los ()
app = FastAPI() 

# Models

class Location(BaseModel): 
    city: str
    state: str
    country: str


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

#validaciones query parametro

@app.get("/person/detail")
def show_person(
     name: Optional[str] = Query(
        None, 
        min_length=1, 
        max_length=50,
        title="Person name",
        description="this is the person name. It's between 1 and 50 chart"
        ),
    age: int = Query(
        ..., 
        title="person age",
        description="This is de person age, it's required"
        ) #aca no se pone el optional porque al poner los ... lo declaramos obligatorio, pero para saber que esta nomas, casi siempre se pone opcional
): 
    return {name: age}

# validation path parameter, van entre {} los query parameters van sin nada como arriba

@app.get("/person/detail/{person_id}") 
def show_person(
    person_id: int = Path(
        ..., 
        gt=0,
        title="It´s person ID",
        description="Person ID required"
        )

    ):
    return {person_id:"it exists"}

# validation requests Body
#con put es para una actualizacion
@app.put("/person/{person_id}")    
def update_person(
    person_id: int = Path(
        ...,
        title="Person ID",
        description="This is the person ID",
        gt=0
    ),
    person: Person = Body(...),
    location: Location = Body(...)
): 
    results = person.dict()
    results.update(location.dict())#aca se usa para combiar los dos body ya que solo se hace de a uno. 
    return results

    
