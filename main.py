#Python
from typing import List, Optional
from enum import Enum #sirve para crear enumeraciones de string, para validar hair_color

#Pydantic
from pydantic import BaseModel
from pydantic import Field, EmailStr  #esto es para validar los models (clases)

#FastApi
from fastapi import FastAPI
from fastapi import Body, Query, Path
from fastapi import status

# esta variable contiene a toda nuestra aplicacion, FastAPI es una instancia por los ()
app = FastAPI() 

# Models

class HairColor(Enum):
    white = 'white'
    black = 'black'
    brown = 'brown'
    blonde = 'blonde'

class Location(BaseModel): 
    city: str = Field(..., min_length=1, max_length=50)
    state: str = Field(..., min_length=1, max_length=50)
    country: Optional[str] = Field(default=None)

    class Config:
        schema_extra = {
            "example": {
                "city": "carmend de areco",
                "state": "bueno aires",
                "country": "Arg"
            }
        }

#aca se aplica la herencia para no repetir codigo, luego en Person y PersonOut tomamos de PersonModel
class PersonModel (BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    age: int = Field(..., gt=0, le=115)
    email : EmailStr = Field(...,)
    hair_color: Optional[HairColor] = Field(default=None)
    is_married: Optional[bool] = Field(default=None)

class Person(PersonModel):
    
    password : str = Field(..., min_length=8)

    #class Config: 
     #    schema_extra = {
      #       "example": {
      #           "first_name": "nicolas",
      #           "last_name": "Dolinkue",
      #           "age": 38, 
      #           "email": "dolinkue_n@hotmail.com",
      #           "hair_color": "blonde",
      #          "is_married": False
                
       #      }
      #   } 

#se crea esta clase para crear un modelo de devolucion sin el password
class PersonOut(PersonModel):  
    pass
    

@app.get(
    path="/", 
    status_code=status.HTTP_200_OK
    )  
def home():
     # para comunicarse se hace mediante Json y en py el Json es un dicci {}
    return {"hello": "world"}   

 # Request and response body
  
 # aca usamos post porque le pedimos al sevidor datos si enviamos seria get
 #dentro de create_person definimos persona con la Person y lo igualamos a body que se importa para poner los ... que dicen que es obligatiro el parametro

# aca se agrega el response_model = PersonOut pq lo que hace es armar todo en base a Person pero devuelve lo que esta en PersonOut es decir sin el Password
@app.post(
    path="/person/new", 
    response_model=PersonOut,
    status_code=status.HTTP_201_CREATED
    ) 
 
def create_person(person: Person = Body(...)):
    return person

#validaciones query parametro

@app.get(
    path="/person/detail",
    status_code=status.HTTP_200_OK
    )
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

@app.get(
    path="/person/detail/{person_id}",
    status_code=status.HTTP_200_OK
    ) 
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
@app.put(
    path="/person/{person_id}",
    status_code=status.HTTP_202_ACCEPTED
    )    
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

    
