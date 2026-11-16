from pydantic import BaseModel, ConfigDict


class CreacionAutor(BaseModel):
    nombre: str
    nacionalidad: str
    email: str


class RespuestaAutor(BaseModel):
    id: int
    nombre: str
    nacionalidad: str
    email: str

    model_config = ConfigDict(from_attributes=True)

class CreacionEditorial(BaseModel):
    nombre: str
    pais: str

class RespuestaEditorial(BaseModel):
    id: int
    nombre: str
    pais: str
    
    model_config = ConfigDict(from_attributes=True)

class CreacionLibro(BaseModel):
    titulo: str
    anio_edicion: int
    precio: float
    autor_id: int
    editorial_id: int


class RespuestaLibro(BaseModel):
    id: int
    titulo: str
    anio_edicion: int
    precio: float
    autor: RespuestaAutor
    editorial: RespuestaEditorial

    model_config = ConfigDict(from_attributes=True)

