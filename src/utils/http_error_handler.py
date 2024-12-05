from fastapi import FastAPI,status
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import Response, JSONResponse
from fastapi.requests import Request
class HTTPErrorHandler(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI) -> None:
        super().__init__(app)

    async def dispatch(self, request: Request, call_next) -> Response|JSONResponse:
       try:
           return await call_next(request)
       except Exception as e:
           content = f"exc:{str(e)}"
           status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
           return JSONResponse(content=content,status_code=status_code)
           