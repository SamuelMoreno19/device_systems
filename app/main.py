from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler

# Importamos tus rutas de la v4.0 (respetando tus alias exactos)
from app.routes import user_routes
from app.routes.device_routes import router as device_router
from app.routes.loan_routes import router as loan_router

# Importamos el nuevo módulo de autenticación
from app.auth import auth_routes

# Importamos el Middleware y el Rate Limiter
from app.middlewares.request_middleware import SecurityAuditMiddleware, limiter

# 🌐 Fase 12 – Configuración de Metadatos Swagger/OpenAPI (Versión 5.0.0)
app = FastAPI(
    title="device_systems API",
    description="API REST segura (v5.0.0) con autenticación JWT, control de roles, políticas CORS, middleware de auditoría y Rate Limiting.",
    version="5.0.0",
    contact={
        "name": "Samuel Moreno"
    }
)

# 🚦 Configurar el manejador global para el Rate Limiting (Fase 11)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Fase 9 – Configuración Estricta de CORS
origins = [
    "http://localhost:5173",  # Entorno estándar Vite
    "http://localhost:3000",  # Entorno estándar React/Next.js
    "http://127.0.0.1:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Fase 10 – Incorporación del Middleware Personalizado de Auditoría
app.add_middleware(SecurityAuditMiddleware)

# Registro de los Módulos de Enrutamiento (Fase 12 - Organizados por Tags)
app.include_router(auth_routes.router)
app.include_router(user_routes.router)
app.include_router(device_router)
app.include_router(loan_router)

# EVENTO STARTUP: Manteniendo tu personalización con los datos de seguridad actualizados
@app.on_event("startup")
def mensaje_encendido():
    print("\n" + "="*70)
    print("SISTEMA DE GESTIÓN DE DISPOSITIVOS (V5.0.0) INICIADO")
    print("Puedes interactuar con la API ingresando a la documentación:")
    print("http://127.0.0.1:8000/docs")
    print("="*70 + "\n")

@app.get("/", tags=["Security"], include_in_schema=False)
def inicio():
    return {
        "status": "online",
        "version": "5.0.0",
        "security_layer": "active",
        "rate_limiting": "enabled"
    }