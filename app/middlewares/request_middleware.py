import time
import uuid
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address

# Inicialización global del Rate Limiter (Fase 11)
# Utiliza la dirección IP del cliente para contar las peticiones
limiter = Limiter(key_func=get_remote_address)

class SecurityAuditMiddleware(BaseHTTPMiddleware):
    """
    Middleware personalizado de auditoría (Fase 10).
    Mide tiempos de procesamiento e inyecta cabeceras obligatorias de seguridad.
    """
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # Generar o propagar un identificador único de rastreo (X-Request-ID)
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4())[:8])
        
        # Procesar la petición y obtener la respuesta del endpoint
        response = await call_next(request)
        
        # Calcular la duración exacta de la transacción
        process_time = time.time() - start_time
        
        # Inyectar en la respuesta las cabeceras requeridas por la guía de la actividad
        response.headers["X-App-Name"] = "device_systems"
        response.headers["X-Process-Time"] = f"{process_time:.4f}"
        response.headers["X-Request-ID"] = request_id
        
        # Log estructurado en la consola estándar del servidor
        print(f"[{request_id}] {request.method} {request.url.path} - Status: {response.status_code} - Time: {process_time:.4f}s")
        
        return response