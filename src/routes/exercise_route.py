from fastapi import APIRouter, HTTPException
from src.schema.exercise_schema import Exercise_Schema
from src.models.connectionExercise_model import ExerciseConnection

exercise_router = APIRouter()
conn = ExerciseConnection()

@exercise_router.post("/", tags=["Exercises"])
def insert_exercise(exercise_data: Exercise_Schema):

    data_tuple = ( 
        exercise_data.name,
        exercise_data.description,
        exercise_data.muscle,
        exercise_data.category,
        exercise_data.videoUrl,
        exercise_data.imageUrl
    )
    try:
        conn.write(data_tuple)
        return {"message": "Ejercicio insertado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al insertar el ejercicio: " + str(e))


@exercise_router.get("/", tags=["Exercises"])
def get_exercises():
    try:
        items = []
        for data in conn.read_all():
            dictionary = {
                "id": data[0],
                "name": data[1],
                "description": data[2],
                "muscle": data[3],
                "category": data[4],
                "videoUrl": data[5],
                "imageUrl": data[6]
            }
            items.append(dictionary)
        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al obtener los ejercicios: " + str(e))

@exercise_router.get("/{id}", tags=["Exercises"])
def get_exercise(id: int):
    dictionary = conn.read_one(id)
    if dictionary is None:
        return {"message": "Ejercicio no encontrado"}
    return dictionary


@exercise_router.delete("/{id}", tags=["Exercises"])
def delete_exercise(id: int):
    try:
        result = conn.delete(id)
        if result:
            return {"message": "Ejercicio eliminado correctamente"}
        else:
            raise HTTPException(status_code=404, detail="Ejercicio no encontrado")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al eliminar el ejercicio: " + str(e))


@exercise_router.put("/{id}", tags=["Exercises"])
def update_exercise(id: int, exercise_data: Exercise_Schema):
    data = (
        exercise_data.name,        
        exercise_data.description,
        exercise_data.muscle,      
        exercise_data.category,         
        id,                          
        exercise_data.videoUrl,      
        exercise_data.imageUrl       
    )
    try:
        result = conn.update(data)
        if result:
            return {"message": "Ejercicio actualizado correctamente"}
        else:
            raise HTTPException(status_code=404, detail="Ejercicio no encontrado")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al actualizar el ejercicio: " + str(e))
