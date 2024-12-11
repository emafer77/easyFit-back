from pydantic import BaseModel

class Categoria_Schema(BaseModel):
    nombre: str
    descripcion: str
