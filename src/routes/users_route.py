from fastapi import APIRouter
from src.schema.user_schema import User_Schema
from src.models.connection_model import UserConnection

conn = UserConnection()
user_router = APIRouter()
@user_router.post("/insert", tags=["Users"])
def insert_user(user_data: User_Schema):
    data_tuple = (
        user_data.nombre,
        user_data.apellidos,
        user_data.correo,
        user_data.contrasena,
        user_data.telefono,
        user_data.edad,
        user_data.genero,
        user_data.peso,
        user_data.altura,
        user_data.objetivo_id,
    )
    conn.write(data_tuple)
    return {"message": "Usuario insertado correctamente"}
@user_router.get("/", tags=["Users"])
def get_users():
   items=[]
   for data in conn.read_all():
       dictionary ={}
       dictionary["id"] = data[0]
       dictionary["nombre"] = data[1]
       dictionary["apellidos"] = data[2]
       dictionary["correo"] = data[3]
       dictionary["contrasena"] = data[4]
       dictionary["telefono"] = data[5]
       dictionary["edad"] = data[6]
       dictionary["genero"] = data[7]
       dictionary["peso"] = data[8]
       dictionary["altura"] = data[9]
       dictionary["objetivo_id"] = data[10]
       items.append(dictionary)
   return items
@user_router.get("/{id}", tags=["Users"])
def get_user(id: int):
    dictionary={}
    data = conn.read_one(id)
    dictionary["id"] = data[0]
    dictionary["nombre"] = data[1]
    dictionary["apellidos"] = data[2]
    dictionary["correo"] = data[3]
    dictionary["contrasena"] = data[4]
    dictionary["telefono"] = data[5]
    dictionary["edad"] = data[6]
    dictionary["genero"] = data[7]
    dictionary["peso"] = data[8]
    dictionary["altura"] = data[9]
    dictionary["objetivo_id"] = data[10]
    return dictionary

@user_router.delete("/{id}", tags=["Users"])
def delete_user(id: int):
    conn.delete(id)
    return {"message": "Usuario eliminado correctamente"}

@user_router.put("/{id}", tags=["Users"])
def update_user(id: int, user_data: User_Schema):
    data =user_data.model_dump()
    data["id"] = id
    conn.update( data)


