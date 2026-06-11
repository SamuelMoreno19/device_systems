from fastapi import FastAPI
from app.database.connection import create_tables
from app.routes import user_routes

app = FastAPI(
    title="device_systems API",
    description="API REST intermedia para la gestión avanzada del recurso usuarios, implementando patrones de arquitectura limpia, manejo de excepciones y Dependency Injection y con Persistencia SQLite v3.0",
    version="3.0.0",
    contact={
        "name": "Samuel Moreno"
    }
)

# NUEVO: Ejecuta la creación automática de tablas en la base de datos al arrancar
create_tables()

app.include_router(user_routes.router)

@app.get("/", tags=["Inicio"], include_in_schema=False)
def inicio():
    return {"mensaje": "Servidor de device_systems V3 activo. Dirígete a /docs"}