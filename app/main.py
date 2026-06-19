from fastapi import FastAPI
from app.database.connection import create_tables
from app.routes import user_routes
from app.routes.device_routes import router as device_router
from app.routes.loan_routes import router as loan_router

app = FastAPI(
    title="device_systems API",
    description="API REST intermedia para la gestión avanzada del recurso usuarios, implementando patrones de arquitectura limpia, manejo de excepciones y Dependency Injection y con Persistencia SQLite v4.0",
    version="4.0.0",
    contact={
        "name": "Samuel Moreno"
    }
)

# NUEVO: Ejecuta la creación automática de tablas en la base de datos al arrancar
create_tables()

app.include_router(user_routes.router)
app.include_router(device_router)
app.include_router(loan_router)

# EVENTO STARTUP: Personaliza el mensaje en la terminal de Uvicorn al encender
@app.on_event("startup")
def mensaje_encendido():
    print("\n" + "="*70)
    print("SISTEMA DE GESTIÓN DE DISPOSITIVOS (V4.0.0) INICIADO EXITOSAMENTE")
    print("Puedes interactuar con la API ingresando a la documentación:")
    print("http://127.0.0.1:8000/docs")
    print("="*70 + "\n")

@app.get("/", tags=["Inicio"], include_in_schema=False)
def inicio():
    return {"mensaje": "Servidor de device_systems V4 activo. Dirígete a /docs"}