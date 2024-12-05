from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse, Response
from src.routes.login_route import login_router
from src.routes.users_route import user_router
from src.routes.exercise_route import exercise_router


app = FastAPI()

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


   
    

       
