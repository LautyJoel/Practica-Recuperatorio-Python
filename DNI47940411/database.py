from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine("sqlite:///database.db")
db_session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


class Autor(Base):
    __tablename__ = "autor"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    nacionalidad = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)

    libros = relationship("Libro", back_populates="autor", cascade="all, delete-orphan")


class Libro(Base):
    __tablename__ = "libro"

    id = Column(Integer, primary_key=True)
    titulo = Column(String(20), nullable=False)
    anio_edicion = Column(Integer, nullable=False)
    precio = Column(Float, nullable=False)
    autor_id = Column(Integer, ForeignKey("autor.id"), nullable=False)
    editorial_id = Column(Integer, ForeignKey("editorial.id"), nullable=False)

    autor = relationship("Autor", back_populates="libros")
    editorial = relationship("Editorial", back_populates="libros")


class Editorial(Base):
    __tablename__ = "editorial"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(20), nullable=False)
    pais = Column(String(20), nullable=False)

    libros = relationship("Libro", back_populates="editorial", cascade="all, delete-orphan")

Base.metadata.create_all(engine, Base.metadata.tables.values(), checkfirst=True)