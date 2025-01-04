from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from src.routes.image import get_router as image_router
from src.routes.menu import get_router as menu_router
from src.routes.orders import get_router as orders_router
from fastapi_metadata import metadata

# FastAPI object
app = FastAPI(prefix="/api/v1", **metadata)

# Configure the exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    ''' Handle validation errors as bad requests '''
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={'detail': 'Invalid request data', 'errors': exc.errors(), 'body': exc.body},
    )

# Add the endpoint routers
app.add_route("/image", image_router())
app.add_route("/menu", menu_router())
app.add_route("/order", orders_router())


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

