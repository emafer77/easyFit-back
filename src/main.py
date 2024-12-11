from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse, Response
from src.routes.login_route import login_router
from src.routes.users_route import user_router
from src.routes.exercise_route import exercise_router
from src.routes.muscle_route import muscle_router
from src.routes.category_route import category_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite solicitudes de cualquier origen
    allow_credentials=True,
    allow_methods=["*"],  # Permite cualquier método (GET, POST, etc.)
    allow_headers=["*"],  # Permite cualquier cabecera
)

# Middleware estándar
@app.middleware("http")
async def http_middleware(request: Request, call_next) -> Response | JSONResponse:
    print('middleware is running')
    response = await call_next(request)
    return response

app.include_router(prefix="/login",router=login_router)
@app.get("/", tags=["home"])
def home():
    return JSONResponse(content="Welcome to my API",status_code=200)
app.include_router(prefix="/users",router=user_router)
app.include_router(prefix="/exercises",router=exercise_router)
app.include_router(prefix="/muscles",router=muscle_router)
app.include_router(prefix="/categories",router=category_router)


   
    

       
