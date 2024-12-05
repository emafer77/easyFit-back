from fastapi import APIRouter, Depends, HTTPException
from src.models.connection_model import UserConnection
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError

login_router = APIRouter()
conn = UserConnection()  

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login/tokens")
SECRET_KEY = "secret"
ALGORITHM = "HS256"


def encode_token(payload: dict) -> str:
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: Annotated[str, Depends(oauth2_scheme)]) -> dict:
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user = next((u for u in conn.read_all() if u[3] == data["correo"]), None)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        
        user_dict = {
            "id": user[0],
            "nombre": user[1],
            "apellidos": user[2],
            "correo": user[3],
            "telefono": user[5],
            "edad": user[6],
            "genero": user[7],
            "peso": user[8],
            "altura": user[9],
            "objetivo_id": user[10]
        }
        return user_dict
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@login_router.post("/tokens", tags=["Login"])
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    users = conn.read_all()  # Lee todos los usuarios de la base de datos
    user = next((u for u in users if u[3] == form_data.username), None)
    if not user or form_data.password != user[4]:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    token = encode_token({"correo": user[3], "nombre": user[1], "id": user[0]})
    return {"access_token": token}

# Ruta protegida para obtener el perfil del usuario autenticado
@login_router.get("/profile", tags=["Login"])
def get_profile(my_user: Annotated[dict, Depends(decode_token)]):
    return my_user
