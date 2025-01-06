import logging
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from src.utils.config import UVICORN_LOG_LEVEL, UVICORN_RELOAD, UVICORN_HOST, UVICORN_PORT
from src.routes.image import get_router as image_router
from src.routes.menu import get_router as menu_router
from src.routes.orders import get_router as orders_router
from fastapi_metadata import metadata

# Set up the logging
logger = logging.getLogger(__name__)

# FastAPI object
app = FastAPI(**metadata)

# CORS middleware - Allow requests from the frontend
origins = [
    "http://127.0.0.1:5173",
    "http://localhost:5173"
]

# Add the CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure the exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    ''' Handle validation errors as bad requests '''
    return JSONResponse(
        status_code = status.HTTP_400_BAD_REQUEST,
        content = {'detail': 'Invalid request data', 'errors': exc.errors(), 'body': exc.body},
    )

# Add the endpoint routers
app.include_router(image_router())
app.include_router(menu_router())
app.include_router(orders_router())


if __name__ == "__main__":
    import uvicorn

    # Run the server
    uvicorn.run(
        app,
        host = UVICORN_HOST,
        port = UVICORN_PORT,
        log_level = UVICORN_LOG_LEVEL,
        reload = UVICORN_RELOAD
    )

