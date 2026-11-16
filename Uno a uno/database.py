
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine("sqlite:///database.db")
db_session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


class Persona(Base):
    __tablename__ = "persona"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)

    pasaporte = relationship("Pasaporte", back_populates="persona", uselist=False, cascade="all, delete-orphan")


class Pasaporte(Base):
    __tablename__ = "pasaporte"

    id = Column(Integer, primary_key=True)
    numero = Column(String(50), unique=True, nullable=False)
    pais_emision = Column(String(100), nullable=False)
    persona_id = Column(Integer, ForeignKey("persona.id"), unique=True, nullable=False)

    persona = relationship("Persona", back_populates="pasaporte")


Base.metadata.create_all(engine, Base.metadata.tables.values(), checkfirst=True)
