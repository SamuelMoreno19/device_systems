# device_systems — API REST con Persistencia SQLite v3.0

API REST construida con **FastAPI** y **SQLAlchemy** para la gestión del recurso `users` dentro del sistema `device_systems`. Esta versión evoluciona la API anterior hacia persistencia real con base de datos SQLite, reemplazando el almacenamiento en memoria por un motor de base de datos relacional con modelos ORM, sesiones controladas y consultas SQL generadas automáticamente.

---

## Tecnologías utilizadas

- **Python 3.x**
- **FastAPI 0.110+** — Framework web moderno y de alto rendimiento
- **Uvicorn 0.28+** — Servidor ASGI para ejecutar la aplicación
- **SQLAlchemy 2.x** — ORM para gestión de la base de datos relacional
- **SQLite** — Base de datos relacional ligera, sin servidor adicional
- **Pydantic v2** — Validación y serialización de datos de entrada/salida
- **email-validator** — Validación de formato de correos electrónicos

---

## Estructura del proyecto

> _Captura de la estructura del proyecto en el editor de código._

![Estructura del proyecto](images/01.png)

```
device_systems/
│── app/
│   │── main.py
│   │── database/
│   │   └── connection.py
│   │── models/
│   │   └── user_model.py
│   │── schemas/
│   │   └── user_schema.py
│   │── routes/
│   │   └── user_routes.py
│   │── services/
│   │   └── user_service.py
│   └── dependencies/
│       └── database_dependency.py
│── device_systems.db
│── requirements.txt
└── README.md
```

---

## Instalación de dependencias

Clona el repositorio e instala las dependencias:

```bash
git clone https://github.com/tu-usuario/device_systems.git
cd device_systems
pip install -r requirements.txt
```

Contenido del `requirements.txt`:

```
fastapi>=0.110.0
uvicorn>=0.28.0
pydantic[email]>=2.6.0
sqlalchemy>=2.0.0
```

---

## Ejecución del servidor

```bash
uvicorn app.main:app --reload
```

Al arrancar, FastAPI ejecuta `create_tables()` automáticamente, lo que crea el archivo `device_systems.db` si no existe y genera la tabla `usuarios` dentro de él.

La API quedará disponible en: [http://127.0.0.1:8000](http://127.0.0.1:8000)

Documentación Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

Documentación ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 🗄️ Base de datos generada

Al ejecutar el servidor por primera vez se genera automáticamente el archivo `device_systems.db` en la raíz del proyecto. Este archivo es la base de datos SQLite que almacena de forma persistente todos los usuarios registrados.

> _Captura del archivo `device_systems.db` generado y su tabla `usuarios` vista desde un cliente SQLite._

![Base de datos generada](images/02.png)

---

## Tabla de endpoints

| Método   | Endpoint                | Descripción                              | Status         |
|----------|-------------------------|------------------------------------------|----------------|
| GET      | `/users`                | Lista todos los usuarios                 | 200 OK         |
| GET      | `/users?role=admin`     | Filtra usuarios por rol                  | 200 OK         |
| GET      | `/users?is_active=true` | Filtra por estado activo                 | 200 OK         |
| GET      | `/users?order_by=name`  | Ordena resultados por nombre o fecha     | 200 OK         |
| GET      | `/users/{user_id}`      | Obtiene un usuario por su ID             | 200 OK         |
| POST     | `/users`                | Registra un nuevo usuario en la DB       | 201 Created    |
| PUT      | `/users/{user_id}`      | Actualización completa de un usuario     | 200 OK         |
| PATCH    | `/users/{user_id}`      | Actualización parcial de un usuario      | 200 OK         |
| DELETE   | `/users/{user_id}`      | Elimina un usuario de la DB              | 204 No Content |

---

## Códigos de estado HTTP utilizados

| Código | Nombre               | Cuándo se usa                                    |
|--------|----------------------|--------------------------------------------------|
| 200    | OK                   | GET, PUT y PATCH exitosos                        |
| 201    | Created              | POST exitoso, usuario creado en la DB            |
| 204    | No Content           | DELETE exitoso, sin cuerpo de respuesta          |
| 400    | Bad Request          | Correo duplicado o PATCH enviado sin datos       |
| 404    | Not Found            | Usuario no encontrado por ID en la DB            |
| 422    | Unprocessable Entity | Datos inválidos detectados por Pydantic          |

---

## 🔍 Ejemplos de peticiones y respuestas

### GET `/users` — Listar todos los usuarios

```
GET http://127.0.0.1:8000/users
```

**Response `200 OK`:**
```json
[
  {
    "id": 1,
    "name": "Samuel Moreno",
    "email": "samuel@mail.com",
    "role": "admin",
    "is_active": true
  }
]
```

---

### GET `/users/{user_id}` — Consultar por ID

```
GET http://127.0.0.1:8000/users/1
```

**Response `200 OK`:**
```json
{
  "id": 1,
  "name": "Samuel Moreno",
  "email": "samuel@mail.com",
  "role": "admin",
  "is_active": true
}
```

---

### POST `/users` — Registrar nuevo usuario

```
POST http://127.0.0.1:8000/users
Content-Type: application/json
```

**Body:**
```json
{
  "name": "Laura Gomez",
  "email": "laura@mail.com",
  "role": "support",
  "is_active": true
}
```

**Response `201 Created`:**
```json
{
  "id": 2,
  "name": "Laura Gomez",
  "email": "laura@mail.com",
  "role": "support",
  "is_active": true
}
```

---

### PUT `/users/{user_id}` — Actualización completa

```
PUT http://127.0.0.1:8000/users/1
Content-Type: application/json
```

**Body:**
```json
{
  "name": "Samuel Moreno Actualizado",
  "email": "samuel_nuevo@mail.com",
  "role": "support",
  "is_active": false
}
```

**Response `200 OK`:**
```json
{
  "id": 1,
  "name": "Samuel Moreno Actualizado",
  "email": "samuel_nuevo@mail.com",
  "role": "support",
  "is_active": false
}
```

---

### PATCH `/users/{user_id}` — Actualización parcial

```
PATCH http://127.0.0.1:8000/users/1
Content-Type: application/json
```

**Body (solo los campos a cambiar):**
```json
{
  "role": "user"
}
```

**Response `200 OK`:**
```json
{
  "id": 1,
  "name": "Samuel Moreno",
  "email": "samuel@mail.com",
  "role": "user",
  "is_active": true
}
```

---

### DELETE `/users/{user_id}` — Eliminar usuario

```
DELETE http://127.0.0.1:8000/users/1
```

**Response `204 No Content`** — Sin cuerpo de respuesta. El registro es eliminado permanentemente de la base de datos.

---

## 🖼️ Capturas

### 1. Estructura del proyecto

> _Vista de la organización de carpetas y archivos del proyecto en el editor de código._

![Estructura del proyecto](images/01.png)

---

### 2. Base de datos generada

> _Archivo `device_systems.db` generado automáticamente al arrancar el servidor, con la tabla `usuarios` visible desde un cliente SQLite._

![Base de datos generada](images/02.png)

---

### 3. Swagger UI — Vista general

> _Vista de todos los endpoints disponibles en la documentación interactiva de FastAPI._

![Swagger UI - Vista general](images/03.png)

---

### 4. GET `/users` — Listar usuarios

> _Evidencia del endpoint GET /users retornando la lista de usuarios desde la base de datos._

![GET /users](images/04.png)

---

### 5. GET `/users/{user_id}` — Consultar por ID

> _Evidencia de la consulta de un usuario específico mediante su ID como Path Parameter._

![GET /users/{user_id}](images/05.png)

---

### 6. POST `/users` — Registrar usuario

> _Evidencia del registro exitoso de un nuevo usuario persistido en la base de datos, con respuesta 201 Created._

![POST /users](images/06.png)

---

### 7. PUT `/users/{user_id}` — Actualización completa

> _Evidencia de la actualización completa de un usuario reemplazando todos sus campos, con respuesta 200 OK._

![PUT /users/{user_id}](images/07.png)

---

### 8. PATCH `/users/{user_id}` — Actualización parcial

> _Evidencia de la actualización parcial enviando solo los campos a modificar, con respuesta 200 OK._

![PATCH /users/{user_id}](images/08.png)

---

### 9. DELETE `/users/{user_id}` — Eliminar usuario

> _Evidencia de la eliminación permanente de un usuario de la base de datos, con respuesta 204 No Content._

![DELETE /users/{user_id}](images/09.png)

---

### 10. Error — Correo duplicado (400)

> _Evidencia del error al intentar registrar un correo ya existente, retornando 400 Bad Request._

![Error correo duplicado](images/10.png)

---

### 11. Error — Datos inválidos (422)

> _Evidencia del error al enviar datos que no cumplen las validaciones de Pydantic, retornando 422 Unprocessable Entity._

![Error datos inválidos](images/11.png)

---

## 🔗 Dependency Injection con `Depends()`

El proyecto usa `Depends()` de FastAPI para reutilizar lógica común entre múltiples endpoints. Las dependencias están en `app/dependencies/database_dependency.py`.

### `get_db` — Ciclo de vida de la sesión

Abre una sesión de base de datos para cada petición y la cierra automáticamente al terminar, sin importar si hubo error o no. Todos los endpoints que necesitan acceder a la DB la inyectan con `Depends(get_db)`.

```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### `get_user_or_404` — Buscar o lanzar 404

Recibe el `user_id` de la URL, ejecuta un `SELECT` en la DB y retorna el usuario si existe. Si no lo encuentra, lanza automáticamente un `404 Not Found` antes de que el endpoint se ejecute.

```python
def get_user_or_404(user_id: int, db: Session = Depends(get_db)) -> Usuario:
    usuario = db.query(Usuario).filter(Usuario.id == user_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="El usuario que buscas no existe.")
    return usuario
```

### `verificar_correo_duplicado` — Validar unicidad del correo

Consulta la DB para verificar que el correo no esté registrado por otro usuario. Acepta un `excluir_id` para que al editar no colisione con el propio correo del usuario que se está modificando.

```python
def verificar_correo_duplicado(email: str, db: Session, excluir_id: int = None):
    query = db.query(Usuario).filter(Usuario.email == email)
    if excluir_id is not None:
        query = query.filter(Usuario.id != excluir_id)
    if query.first():
        raise HTTPException(status_code=400, detail="Ese correo ya existe, intenta con otro.")
```

---

## Manejo de errores implementado

| Escenario                      | Código | Mensaje de respuesta                                        |
|--------------------------------|--------|-------------------------------------------------------------|
| Usuario no encontrado          | 404    | `"El usuario que buscas no existe."`                        |
| Correo electrónico duplicado   | 400    | `"Ese correo ya existe, intenta con otro."`                 |
| PATCH enviado sin ningún campo | 400    | `"Intento de actualización sin datos. Debe enviar al menos un campo."` |
| Datos inválidos (Pydantic)     | 422    | Detalle automático de FastAPI con el campo inválido         |

Todos los errores retornan:

```json
{
  "detail": "Mensaje descriptivo del error"
}
```

---

## Diferencia entre Modelo SQLAlchemy y Schema Pydantic

En este proyecto conviven dos tipos de "modelos" que cumplen roles completamente distintos dentro de la arquitectura.

### Modelo SQLAlchemy — `app/models/user_model.py`

Representa la **estructura de la tabla en la base de datos**. Hereda de `Base` y le dice a SQLAlchemy cómo mapear una clase Python a una tabla SQL real. Sus atributos son columnas (`Column`) con tipos de datos de la DB (`Integer`, `String`, `Boolean`).

```python
class Usuario(Base):
    __tablename__ = "usuarios"
    id       = Column(Integer, primary_key=True, autoincrement=True)
    name     = Column(String, nullable=False)
    email    = Column(String, unique=True, nullable=False)
    role     = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
```

Su responsabilidad es **hablar con la base de datos**: leer, insertar, actualizar y eliminar registros.

---

### Schema Pydantic — `app/schemas/user_schema.py`

Representa las **reglas de validación de los datos que entran y salen de la API**. Hereda de `BaseModel` y define qué campos acepta el cliente, con qué formato y con qué restricciones. No sabe nada de la base de datos.

```python
class UserCreate(BaseModel):
    name:      str = Field(..., min_length=3)
    email:     EmailStr
    role:      Literal["admin", "support", "user"]
    is_active: bool = True
```

Su responsabilidad es **hablar con el cliente HTTP**: validar lo que llega en el body del request y moldear lo que se retorna en la respuesta.

---

### Resumen de la diferencia

| Característica        | Modelo SQLAlchemy (`Usuario`)     | Schema Pydantic (`UserCreate`)     |
|-----------------------|-----------------------------------|------------------------------------|
| Hereda de             | `Base` (SQLAlchemy)               | `BaseModel` (Pydantic)             |
| Representa            | Una tabla en la base de datos     | Datos de entrada/salida de la API  |
| Responsabilidad       | Persistencia y consultas SQL      | Validación y serialización HTTP    |
| Conoce la DB          | ✅ Sí                             | ❌ No                              |
| Valida datos del cliente | ❌ No                          | ✅ Sí                              |

Usar ambos en capas separadas es una práctica profesional: el schema protege la entrada de datos, y el modelo gestiona su almacenamiento.

---

## Reflexión sobre la importancia de usar persistencia en una API

El cambio más significativo en esta versión del proyecto fue migrar de una lista en memoria a una base de datos real con SQLAlchemy y SQLite, y esa diferencia se nota de inmediato en la robustez de la API.

Con el almacenamiento en memoria, cada vez que se reiniciaba el servidor todos los datos desaparecían. Era útil para aprender la estructura de FastAPI, pero completamente inviable en un escenario real. Incorporar persistencia con SQLite cambió eso: los usuarios registrados sobreviven a los reinicios, pueden ser consultados, actualizados y eliminados de forma confiable, y el historial de datos se mantiene intacto.

SQLAlchemy también trajo otra ventaja que no esperaba: permite trabajar con la base de datos usando Python puro, sin escribir SQL manualmente. El ORM traduce las operaciones (`db.query()`, `db.add()`, `db.commit()`) a sentencias SQL reales de forma automática, lo que reduce errores y hace el código más legible.

Finalmente, entender la separación entre el modelo ORM y el schema Pydantic fue clave. Al principio parece redundante tener dos representaciones del mismo "usuario", pero en la práctica cada uno cumple un rol bien definido: Pydantic protege lo que entra por HTTP, y SQLAlchemy gestiona lo que se guarda en disco. Esa separación de responsabilidades es lo que hace que una API sea mantenible a largo plazo.

---

## Cabeceras HTTP personalizadas

Todos los endpoints retornan las siguientes cabeceras personalizadas:

```
X-App-Name: device_systems
X-API-Version: 2.0
```
