from fastapi import FastAPI
from app.api.auth import router as auth_router
from app.api.users import router as users_router
from fastapi.openapi.utils import get_openapi
from app.api.listings import router as listings_router
from app.api.categories import router as categories_router
from app.api.messages import router as messages_router
app = FastAPI()

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



