
from fastapi import FastAPI, HTTPException, status

from database import Persona, Pasaporte, db_session
from schema import (
    CreacionPersona,
    CreacionPasaporte,
    RespuestaPersona,
    RespuestaPasaporte,
)

app = FastAPI()


@app.middleware("http")
def cerrar_sesion_bd(request, call_next):
    try:
        return call_next(request)
    finally:
        db_session.remove()


# ---------------- PERSONAS ----------------

@app.get("/personas", response_model=list[RespuestaPersona])
def obtener_personas():
    try:
        return Persona.query.all()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener las personas: {e}",
        )


@app.get("/personas/{persona_id}", response_model=RespuestaPersona)
def obtener_persona(persona_id: int):
    try:
        persona = Persona.query.get(persona_id)

        if not persona:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Persona no encontrada",
            )

        return persona
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener la persona: {e}",
        )


@app.post(
    "/personas",
    status_code=status.HTTP_201_CREATED,
    response_model=RespuestaPersona,
)
def crear_persona(persona_data: CreacionPersona):
    try:
        persona = Persona(
            nombre=persona_data.nombre,
            email=persona_data.email
        )

        db_session.add(persona)
        db_session.commit()
        db_session.refresh(persona)

        return persona
    except Exception as e:
        db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear la persona: {e}",
        )


# ---------------- PASAPORTES ----------------

@app.get("/pasaportes", response_model=list[RespuestaPasaporte])
def obtener_pasaportes():
    try:
        return Pasaporte.query.all()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener los pasaportes: {e}",
        )


@app.get("/pasaportes/{pasaporte_id}", response_model=RespuestaPasaporte)
def obtener_pasaporte(pasaporte_id: int):
    try:
        pasaporte = Pasaporte.query.get(pasaporte_id)

        if not pasaporte:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pasaporte no encontrado",
            )

        return pasaporte
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener el pasaporte: {e}",
        )


@app.post(
    "/pasaportes",
    status_code=status.HTTP_201_CREATED,
    response_model=RespuestaPasaporte,
)
def crear_pasaporte(pasaporte_data: CreacionPasaporte):
    try:
        persona = Persona.query.get(pasaporte_data.persona_id)

        if not persona:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Persona no encontrada",
            )

        pasaporte_existente = Pasaporte.query.filter_by(
            persona_id=pasaporte_data.persona_id
        ).first()

        if pasaporte_existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La persona ya tiene un pasaporte",
            )

        pasaporte = Pasaporte(
            numero=pasaporte_data.numero,
            pais_emision=pasaporte_data.pais_emision,
            persona_id=pasaporte_data.persona_id
        )

        db_session.add(pasaporte)
        db_session.commit()
        db_session.refresh(pasaporte)

        return pasaporte

    except HTTPException:
        raise
    except Exception as e:
        db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear el pasaporte: {e}",
        )


# ---------------- RELACION UNO A UNO ----------------

# OBTENER PASAPORTE DE UNA PERSONA
@app.get(
    "/personas/{persona_id}/pasaporte",
    response_model=RespuestaPasaporte,
)
def obtener_pasaporte_persona(persona_id: int):
    try:
        persona = Persona.query.get(persona_id)

        if not persona:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Persona no encontrada",
            )

        pasaporte = Pasaporte.query.filter_by(
            persona_id=persona_id
        ).first()

        if not pasaporte:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="La persona no tiene pasaporte",
            )

        return pasaporte

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener el pasaporte: {e}",
        )


# ELIMINAR PASAPORTE
@app.delete("/pasaportes/{pasaporte_id}")
def eliminar_pasaporte(pasaporte_id: int):
    try:
        pasaporte = Pasaporte.query.get(pasaporte_id)

        if not pasaporte:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pasaporte no encontrado",
            )

        db_session.delete(pasaporte)
        db_session.commit()

        return {"mensaje": "Pasaporte eliminado"}

    except HTTPException:
        raise
    except Exception as e:
        db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar el pasaporte: {e}",
        )
