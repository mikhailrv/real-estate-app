from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.controllers.auth import router as auth_router
from app.controllers.users import router as users_router
from fastapi.openapi.utils import get_openapi
from app.controllers.listings import router as listings_router
from app.controllers.categories import router as categories_router
from app.controllers.messages import router as messages_router
from app.controllers.property_types import router as property_types_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

origins = [
    "http://localhost",
    "http://127.0.0.1",
    "http://localhost:19000",  
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Циан",
        version="1.0.0",
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return openapi_schema

app.openapi = custom_openapi

app.include_router(messages_router)
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(listings_router)
app.include_router(categories_router)
app.include_router(property_types_router)


