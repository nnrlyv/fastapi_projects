from fastapi import FastAPI
import logging
import time
from fastapi.requests import Request



logger = logging.getLogger("uvicorn.access")
logger.disabled = True

def register_middleware(app: FastAPI):
    @app.middleware("http")
    async def custom_logging(request:Request,call_next):
        start_time = time.perf_counter()

        response = await call_next(request)
        end_time = time.perf_counter() - start_time

        message = f"{request.client.host}: {request.client.port} - {request.method} - {request.url.path} - {response.status_code} completed after {end_time}s"

        print(message)
        return response