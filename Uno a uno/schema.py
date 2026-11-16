
from pydantic import BaseModel, ConfigDict


class CreacionPersona(BaseModel):
    nombre: str
    email: str


class RespuestaPersona(BaseModel):
    id: int
    nombre: str
    email: str

    model_config = ConfigDict(from_attributes=True)


class CreacionPasaporte(BaseModel):
    numero: str
    pais_emision: str
    persona_id: int


class RespuestaPasaporte(BaseModel):
    id: int
    numero: str
    pais_emision: str
    persona_id: int

    model_config = ConfigDict(from_attributes=True)

