from fastapi import FastAPI, HTTPException, status

from database import Autor, Libro, Editorial, db_session
from schema import (
    CreacionAutor,
    CreacionLibro,
    CreacionEditorial,
    RespuestaAutor,
    RespuestaLibro,
    RespuestaEditorial,
)

app = FastAPI()


@app.middleware("http")
def cerrar_sesion_bd(request, call_next):
    try:
        return call_next(request)
    finally:
        db_session.remove()


@app.get("/autores", response_model=list[RespuestaAutor])
def obtener_autores():
    try:
        return Autor.query.all()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocurrió un error al intentar obtener los autores: {e}",
        )

#T1-1-1
@app.get("/autores/{autor_id}", response_model=RespuestaAutor)
def obtener_autor(autor_id: int):
    try:
        autor = Autor.query.get(autor_id)

        if not autor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Autor no encontrado",
            )

        return autor
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener el autor: {e}",
        )

#T1-1-2
@app.put("/autores/{autor_id}", response_model=RespuestaAutor)
def actualizar_autor(autor_id: int, autor_data: CreacionAutor):
    try:
        autor = Autor.query.get(autor_id)

        if not autor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Autor no encontrado",
            )

        autor.nombre = autor_data.nombre
        autor.nacionalidad = autor_data.nacionalidad
        autor.email = autor_data.email

        db_session.commit()
        db_session.refresh(autor)

        return autor
    except HTTPException:
        raise
    except Exception as e:
        db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar el autor: {e}",
        )

#T1-1-3
@app.delete("/autores/{autor_id}")
def eliminar_autor(autor_id: int):
    try:
        autor = Autor.query.get(autor_id)

        if not autor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Autor no encontrado",
            )

        db_session.delete(autor)
        db_session.commit()

        return {"mensaje": "Autor eliminado"}
    except HTTPException:
        raise
    except Exception as e:
        db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar el autor: {e}",
        )

@app.post(
    "/autores",
    status_code=status.HTTP_201_CREATED,
    response_model=RespuestaAutor,
)
def crear_autor(autor_data: CreacionAutor):
    try:
        autor = Autor(
            nombre=autor_data.nombre,
            nacionalidad=autor_data.nacionalidad,
            email=autor_data.email
        )

        db_session.add(autor)
        db_session.commit()
        db_session.refresh(autor)

        return autor
    except Exception as e:
        db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocurrió un error al intentar crear el autor: {e}",
        )


@app.get("/libros", response_model=list[RespuestaLibro])
def obtener_libros():
    try:
        return Libro.query.all()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocurrió un error al intentar obtener los libros: {e}",
        )


@app.get("/libros/{libro_id}", response_model=RespuestaLibro)
def obtener_libro(libro_id: int):
    try:
        libro = Libro.query.get(libro_id)

        if not libro:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Libro no encontrado",
            )

        return libro
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocurrió un error al intentar obtener el libro con ID {libro_id}: {e}",
        )


@app.post("/libros", status_code=status.HTTP_201_CREATED, response_model=RespuestaLibro)
def crear_libro(libro_data: CreacionLibro):
    try:
        autor = Autor.query.get(libro_data.autor_id)

        if not autor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="El autor no existe",
            )
            
        editorial = Editorial.query.get(libro_data.editorial_id)

        if not editorial:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="La editorial no existe",
        )
        
        libro = Libro(
            titulo=libro_data.titulo,
            anio_edicion=libro_data.anio_edicion,
            precio=libro_data.precio,
            autor_id=libro_data.autor_id,
            editorial_id=libro_data.editorial_id
        )

        db_session.add(libro)
        db_session.commit()
        db_session.refresh(libro)

        return libro
    except HTTPException:
        raise
    except Exception as e:
        db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocurrió un error al intentar crear el libro: {e}",
        )



@app.put("/libros/{libro_id}", response_model=RespuestaLibro)
def actualizar_libro(libro_id: int, libro_data: CreacionLibro):
    try:
        libro = Libro.query.get(libro_id)

        if not libro:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Libro no encontrado",
            )

        autor = Autor.query.get(libro_data.autor_id)

        if not autor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="El autor no existe",
            )
            
        editorial = Editorial.query.get(libro_data.editorial_id)

        if not editorial:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="La editorial no existe",
            )

        libro.titulo = libro_data.titulo
        libro.anio_edicion = libro_data.anio_edicion
        libro.precio = libro_data.precio
        libro.autor_id = libro_data.autor_id
        libro.editorial_id = libro_data.editorial_id

        db_session.commit()
        db_session.refresh(libro)

        return libro
    except HTTPException:
        raise
    except Exception as e:
        db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocurrió un error al intentar actualizar el libro con ID {libro_id}: {e}",
        )


@app.delete("/libros/{libro_id}")
def eliminar_libro(libro_id: int):
    try:
        libro = Libro.query.get(libro_id)

        if not libro:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Libro no encontrado",
            )

        db_session.delete(libro)
        db_session.commit()

        return {"mensaje": "Libro eliminado"}
    except HTTPException:
        raise
    except Exception as e:
        db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocurrió un error al intentar eliminar el libro con ID {libro_id}: {e}",
        )


#T1-2-1
@app.get("/editoriales", response_model=list[RespuestaEditorial])
def obtener_editoriales():
    try:
        return Editorial.query.all()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener las editoriales: {e}",
        )

#T1-2-2
@app.get("/editoriales/{editorial_id}", response_model=RespuestaEditorial)
def obtener_editorial(editorial_id: int):
    try:
        editorial = Editorial.query.get(editorial_id)

        if not editorial:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Editorial no encontrada",
            )

        return editorial
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener la editorial: {e}",
        )

#T1-2-3
@app.post(
    "/editoriales",
    status_code=status.HTTP_201_CREATED,
    response_model=RespuestaEditorial,
)
def crear_editorial(editorial_data: CreacionEditorial):
    try:
        editorial = Editorial(
            nombre=editorial_data.nombre,
            pais=editorial_data.pais
        )

        db_session.add(editorial)
        db_session.commit()
        db_session.refresh(editorial)

        return editorial
    except Exception as e:
        db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear la editorial: {e}",
        )


#CONSULTAS DEL PARCIAL
#OBTENER LIBROS DE UNA EDITORIAL POR ID
@app.get("/editoriales/{editorial_id}/libros", response_model=list[RespuestaLibro])
def obtener_libros_de_editorial(editorial_id: int):
    try:
        editorial_encontrada = Editorial.query.get(editorial_id)
        if not editorial_encontrada:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Editorial no encontrada",
            )

        libros = Libro.query.filter_by(editorial_id=editorial_id).all()
        return libros
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocurrió un error al intentar obtener los libros de la editorial con ID {editorial_id}: {e}",
        )

#OBTENER LIBROS POR AÑO DE EDICION 
@app.get("/libros/edicion-superior/{anio}", response_model=list[RespuestaLibro])
def obtener_libros_por_anio(anio: int):
    try:
        libros = Libro.query.filter(Libro.anio_edicion > anio).all()
        return libros
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocurrió un error al intentar obtener los libros con año de edición superior a {anio}: {e}",
        )

#OBTENER LIBROS POR PRECIO
@app.get("/libros/mayor-precio/", response_model=list[RespuestaLibro])
def obtener_libros_por_precio():
    try:
        libros = Libro.query.order_by(Libro.precio.desc()).all()
        return libros
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocurrió un error al intentar obtener los libros ordenados por precio: {e}",
        )

 
#CONSULTAS DE CHAT
#Buscar libros publicados después de un año determinado
@app.get("/libros/recientes", response_model=list[RespuestaLibro])
def obtener_libros_recientes():
    try:
        libros = Libro.query.filter(
            Libro.anio_edicion > 2000
        ).order_by(
            Libro.anio_edicion.desc()
        ).all()

        return libros

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener los libros recientes: {e}",
        )
        
#Buscar libros dentro de un rango de precios
@app.get("/libros/precios", response_model=list[RespuestaLibro])
def obtener_libros_por_precio():
    try:
        libros = Libro.query.filter(
            Libro.precio >= 10000,
            Libro.precio <= 30000
        ).all()

        return libros

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al filtrar libros por precio: {e}",
        )
        
#Buscar libros cuyo título contenga una palabra
@app.get("/libros/buscar", response_model=list[RespuestaLibro])
def buscar_libros():
    try:
        libros = Libro.query.filter(
            Libro.titulo.like("%amor%")
        ).all()

        return libros

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al buscar libros: {e}",
        )
        
#Obtener los 3 libros más caros
@app.get("/libros/mas-caros", response_model=list[RespuestaLibro])
def obtener_libros_mas_caros():
    try:
        libros = Libro.query.order_by(
            Libro.precio.desc()
        ).limit(3).all()

        return libros

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener los libros más caros: {e}",
        )
        
#Buscar libros de autores argentinos o colombianos
@app.get("/libros/nacionalidades", response_model=list[RespuestaLibro])
def obtener_libros_por_nacionalidad():
    try:
        libros = Libro.query.join(Autor).filter(
            or_(
                Autor.nacionalidad == "Argentina",
                Autor.nacionalidad == "Colombiana"
            )
        ).all()

        return libros

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener los libros: {e}",
        )
        
#Buscar autores de una nacionalidad
@app.get("/autores/argentinos", response_model=list[RespuestaAutor])
def obtener_autores_argentinos():
    try:
        autores = Autor.query.filter_by(
            nacionalidad="Argentina"
        ).all()

        return autores

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener los autores: {e}",
        )
        
#Buscar autores cuyo nombre contenga una letra o palabra
@app.get("/autores/buscar", response_model=list[RespuestaAutor])
def buscar_autores():
    try:
        autores = Autor.query.filter(
            Autor.nombre.like("%gabriel%")
        ).all()

        return autores

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al buscar autores: {e}",
        )
        
#Obtener autores ordenados alfabéticamente
@app.get("/autores/ordenados", response_model=list[RespuestaAutor])
def obtener_autores_ordenados():
    try:
        autores = Autor.query.order_by(
            Autor.nombre.asc()
        ).all()

        return autores

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al ordenar autores: {e}",
        )
        
#Calcular el valor total de los libros de cada editorial
@app.get("/editoriales/valor-libros")
def obtener_valor_libros_editorial():
    try:
        resultado = db_session.query(
            Editorial.nombre,
            func.sum(Libro.precio).label("valor_total")
        ).join(
            Libro
        ).group_by(
            Editorial.id
        ).all()

        return resultado

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al calcular el valor de los libros: {e}",
        )
        
#Obtener los 5 libros más baratos de una editorial
@app.get("/editoriales/{editorial_id}/libros-baratos", response_model=list[RespuestaLibro])
def obtener_libros_baratos(editorial_id: int):
    try:
        editorial = Editorial.query.get(editorial_id)

        if not editorial:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Editorial no encontrada",
            )

        libros = Libro.query.filter_by(
            editorial_id=editorial_id
        ).order_by(
            Libro.precio.asc()
        ).limit(5).all()

        return libros

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener los libros: {e}",
        )
        
#Obtener autores que tengan más de un libro
@app.get("/autores/con-varios-libros")
def obtener_autores_con_varios_libros():
    try:
        resultado = db_session.query(
            Autor.nombre,
            func.count(Libro.id).label("cantidad")
        ).join(
            Libro
        ).group_by(
            Autor.id
        ).having(
            func.count(Libro.id) > 1
        ).all()

        return resultado

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener autores: {e}",
        )