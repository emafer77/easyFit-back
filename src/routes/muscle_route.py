from fastapi import APIRouter, HTTPException
from src.schema.muscle_schema import Muscle_Schema
from src.models.connectionMuscle_model import MusculoConnection

muscle_router = APIRouter()
conn = MusculoConnection()

@muscle_router.post("/insert", tags=["Muscles"])
def insert_muscle(muscle_data: Muscle_Schema):
    try:
        new_id = conn.create(muscle_data.name)
        return {"message": "Músculo insertado correctamente", "id": new_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al insertar el músculo: " + str(e))


@muscle_router.get("/", tags=["Muscles"])
def get_muscles():
    try:
        muscles = []
        for data in conn.read_all():
            muscles.append({
                "id": data[0],
                "name": data[1]
            })
        return muscles
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al obtener los músculos: " + str(e))


@muscle_router.get("/{id}", tags=["Muscles"])
def get_muscle(id: int):
    muscle = conn.read_one(id)
    if not muscle:
        raise HTTPException(status_code=404, detail="Músculo no encontrado")
    return muscle


@muscle_router.put("/{id}", tags=["Muscles"])
def update_muscle(id: int, muscle_data: Muscle_Schema):
    try:
        result = conn.update(id, muscle_data.name)
        if result:
            return {"message": "Músculo actualizado correctamente"}
        else:
            raise HTTPException(status_code=404, detail="Músculo no encontrado")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al actualizar el músculo: " + str(e))


@muscle_router.delete("/{id}", tags=["Muscles"])
def delete_muscle(id: int):
    try:
        result = conn.delete(id)
        if result:
            return {"message": "Músculo eliminado correctamente"}
        else:
            raise HTTPException(status_code=404, detail="Músculo no encontrado")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al eliminar el músculo: " + str(e))
