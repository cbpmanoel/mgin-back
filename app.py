from fastapi import FastAPI
from .src.routes.image import get_router as image_router
from .src.routes.menu import get_router as menu_router
from .src.routes.orders import get_router as orders_router

# FastAPI object
app = FastAPI(title="MGin Kiosk API", description="API for MGin Kiosk", version="0.1", prefix="/api")

# Add the endpoint routers
app.add_route("/image", image_router())
app.add_route("/menu", menu_router())
app.add_route("/order", orders_router())


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

