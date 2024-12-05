from pydantic import BaseModel, EmailStr
from typing import Optional


class User_Schema(BaseModel):
   nombre: str
   apellidos: str
   correo: EmailStr
   contrasena: str  
   telefono: Optional[str] 
   edad: Optional[int] 
   genero: Optional[str] 
   peso: Optional[float] 
   altura: Optional[float] 
   objetivo_id: Optional[int] 
   model_config = {
       "json_schema_extra": {
           "example": {
               "nombre": "John",
               "apellidos": "Doe",
               "correo": "K0m9o@example.com",
               "contrasena": "password123",
               "telefono": "1234567890",
               "edad": 25,
               "genero": "M",
               "peso": 80,
               "altura": 175,
               "objetivo_id": 1
           }
       }
   }

