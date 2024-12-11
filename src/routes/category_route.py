from fastapi import APIRouter, HTTPException
from src.schema.category_schema import Categoria_Schema  # Asegúrate de crear el esquema de categorías
from src.models.connectionCategory_model import CategoriaEjercicioConnection

category_router = APIRouter()
conn = CategoriaEjercicioConnection()

@category_router.post("/insert", tags=["Categories"])
def insert_category(categoria_data: Categoria_Schema):
    try:
        new_id = conn.create(categoria_data.nombre, categoria_data.descripcion)
        return {"message": "Categoría insertada correctamente", "id": new_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al insertar la categoría: " + str(e))


@category_router.get("/", tags=["Categories"])
def get_categories():
    try:
        categories = []
        for data in conn.read_all():
            categories.append({
                "id": data[0],
                "name": data[1],
                "description": data[2]
            })
        return categories
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al obtener las categorías: " + str(e))


@category_router.get("/{id}", tags=["Categories"])
def get_category(id: int):
    category = conn.read_one(id)
    if not category:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return category


@category_router.put("/{id}", tags=["Categories"])
def update_category(id: int, categoria_data: Categoria_Schema):
    try:
        result = conn.update(id, categoria_data.nombre, categoria_data.descripcion)
        if result:
            return {"message": "Categoría actualizada correctamente"}
        else:
            raise HTTPException(status_code=404, detail="Categoría no encontrada")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al actualizar la categoría: " + str(e))


@category_router.delete("/{id}", tags=["Categories"])
def delete_category(id: int):
    try:
        result = conn.delete(id)
        if result:
            return {"message": "Categoría eliminada correctamente"}
        else:
            raise HTTPException(status_code=404, detail="Categoría no encontrada")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al eliminar la categoría: " + str(e))
