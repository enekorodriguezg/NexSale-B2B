# NexSale-B2B

[English](README.md) · **Español**

> 🚧 **Proyecto en desarrollo.** Usuarios, productos y pedidos tienen CRUD completo y las funciones de seguridad ya están implementadas; quedan algunos puntos pendientes (ver [Próximos pasos](#próximos-pasos)).

Backend transaccional para la gestión de pedidos y ventas entre empresas (B2B). Es una API REST construida con **FastAPI** que gestiona usuarios con distintos roles, un catálogo de productos con control de stock, pedidos de clientes con flujo de estados y generación de facturas, todo desplegado con **Docker Compose** detrás de **Apache** como proxy inverso.

Desarrollado para la asignatura *Component-Oriented Programming* (Programación Orientada a Componentes) de la Universidad de Ciencias Aplicadas de Zagreb (TVZ).

## Funcionalidades

- **Autenticación con JWT** (flujo OAuth2 por contraseña) con sesiones de 8 horas.
- **Control de acceso por roles**, con tres roles:

  | Rol | Permisos |
  |---|---|
  | `admin` | Todo, incluidos usuarios, ajustes y eliminar pedidos |
  | `commercial` | Consultar el catálogo, crear pedidos y gestionar **sus propios** pedidos |
  | `warehouse` | Gestionar productos, stock e imágenes de producto |

- **Gestión de usuarios** (admin): alta, edición, borrado y **desactivación** de usuarios. Un usuario desactivado no puede iniciar sesión, y sus sesiones abiertas dejan de funcionar al momento. Un admin no puede borrar, desactivar ni cambiar el rol de su propia cuenta.
- **Catálogo de productos**: CRUD completo, ordenación, filtrado por categoría, estado de stock calculado e imágenes guardadas como BLOB (`MEDIUMBLOB`, hasta 16 MB).
- **Pedidos**:
  - Varias líneas por pedido, con comprobación y descuento de stock dentro de una única transacción.
  - Flujo de estados `pending → shipped → completed`, o `cancelled`. Los pedidos completados y cancelados son estados finales.
  - Cancelar o borrar un pedido abierto devuelve su stock.
  - Ordenación y filtrado por nombre de cliente.
  - Validación del identificador fiscal del cliente (OIB croata).
- **Facturas**: cualquier pedido se puede descargar como factura en **PDF** o **RTF** (cabecera del pedido + líneas). Todas las facturas van **firmadas digitalmente** (RSA-PSS + SHA-256); la firma se envía en la cabecera `X-Signature` de la respuesta y se puede comprobar con `/security/verify`. La generación concurrente de informes está limitada con un semáforo, y un mutex protege el contador compartido de informes activos.
- **Concurrencia segura**: las filas de stock se bloquean con `SELECT … FOR UPDATE` en un orden fijo, para evitar la sobreventa y los interbloqueos.
- **Tarifa de precios exportable (JSON)**: el catálogo se puede exportar a `data/catalog.json`, y sus productos se pueden leer, editar y borrar **en ese archivo** sin tocar la base de datos (un lock evita las actualizaciones perdidas).
- **Ajustes de la aplicación en un archivo INI** (`config/settings.ini`): nombre de la empresa y moneda de las facturas, y el umbral de stock bajo. El admin puede consultarlos y cambiarlos en caliente.
- **Seguridad**:
  - Contraseñas con hash SHA-256, sal individual por usuario y *pepper* global.
  - El identificador fiscal del cliente se guarda **cifrado con AES-256-GCM**, de forma transparente, mediante un tipo de columna propio de SQLAlchemy.
  - **Buzón seguro con RSA-2048 (OAEP)**: la API publica su clave pública para que los clientes envíen datos cifrados que solo el servidor puede leer.
  - **Firma digital** (RSA-PSS): las facturas se firman con la clave privada del servidor, y cualquier usuario con sesión puede verificar su autoría e integridad.
- **Portal web**: frontend HTML ligero servido por Apache.
- **Documentación interactiva de la API** generada por FastAPI en `/docs` y `/redoc`.

## Tecnologías

| Capa | Tecnología |
|---|---|
| API | Python 3.11, FastAPI, Pydantic, Uvicorn |
| Persistencia | SQLAlchemy 2, MySQL 8 (PyMySQL) |
| Seguridad | PyJWT, `hashlib` (SHA-256 + sal + *pepper*), `cryptography` (AES-256-GCM, RSA-OAEP, RSA-PSS) |
| Informes | fpdf2 (PDF), RTF |
| Configuración y archivos | python-dotenv (`.env`), `configparser` (INI), `json` |
| Infraestructura | Docker, Docker Compose, Apache httpd 2.4 (proxy inverso) |

## Arquitectura

```text
              ┌────────────────────────────── nexsale_net ──────────────────────────────┐
 Navegador ──►│  Apache :80  ──(/auth, /products, /orders, /users,  ──►  FastAPI :8000  │
              │     │            /settings, /security, /docs)                │          │
              │     └── sirve frontend/index.html                            ▼          │
              │                                                         MySQL :3306     │
              └─────────────────────────────────────────────────────────────────────────┘
```

El código está organizado por capas (router → servicio → modelo):

```text
server/
├── main.py          Punto de entrada y registro de routers
├── routers/         Endpoints HTTP (auth, users, products, orders, catalog, settings, security)
├── services/        Lógica de negocio (pedidos, stock, usuarios, informes, archivos del catálogo, ajustes, seguridad)
├── schemas/         Modelos Pydantic de validación y respuesta
├── models.py        Modelos ORM de SQLAlchemy (+ tipo de columna cifrada)
├── constants.py     Roles de usuario y estados de pedido
├── api/deps.py      Dependencias: usuario actual, RoleChecker
└── core/            Configuración y seguridad
    ├── config.py        Variables de entorno y validación de claves
    ├── security.py      Hash de contraseñas y JWT
    ├── crypto.py        Cifrado AES-256-GCM
    ├── rsa_crypto.py    Claves RSA, cifrado OAEP y firmas PSS
    └── app_settings.py  Ajustes en INI
frontend/            Portal web estático
apache/              Imagen y virtual host del proxy inverso
scripts/             Carga inicial, generación de claves RSA y cliente de demostración
config/              Archivo de ajustes (se genera al arrancar, no se versiona)
data/                Archivos exportados del catálogo (se generan, no se versionan)
keys/                Par de claves RSA (se genera, nunca se versiona)
```

## Puesta en marcha

**Requisitos:** Docker y Docker Compose.

1. Clona el repositorio:

   ```bash
   git clone https://github.com/enekorodriguezg/NexSale-B2B.git
   cd NexSale-B2B
   ```

2. Crea el fichero de entorno y rellena todos los valores:

   ```bash
   cp .env.example .env
   ```

   | Variable | Descripción |
   |---|---|
   | `MYSQL_ROOT_PASSWORD`, `MYSQL_DATABASE`, `MYSQL_USER`, `MYSQL_PASSWORD` | Credenciales de MySQL |
   | `MYSQL_PORT` | Puerto de MySQL (déjalo en `3306`: la API también lo usa para conectarse) |
   | `PEPPER` | Secreto que se añade a todas las contraseñas antes del hash |
   | `SECRET_KEY` | Clave con la que se firman los JWT (mínimo 32 caracteres) |
   | `AES_KEY` | Clave AES de 32 bytes en Base64. **Sin ella, la API no arranca.** |
   | `RSA_KEYS_DIR`, `SETTINGS_FILE_PATH`, `DATA_DIR` | Opcionales: ubicación de las claves RSA, del archivo INI y de los archivos exportados |

   Los comentarios de `.env.example` indican cómo generar cada clave, por ejemplo:

   ```bash
   python -c "import os, base64; print(base64.b64encode(os.urandom(32)).decode())"
   ```

3. Construye y arranca los servicios:

   ```bash
   docker compose up --build
   ```

4. Genera el par de claves RSA (solo una vez):

   ```bash
   docker compose exec nexsale_api python scripts/generate_rsa_keys.py
   ```

   Las claves se guardan en `keys/` mediante un volumen de Docker, así que se conservan al reconstruir. El script se niega a sobrescribir unas claves existentes.

5. Abre:
   - Portal web: <http://localhost>
   - Documentación de la API: <http://localhost/docs>

Al arrancar, la API crea las tablas, genera `config/settings.ini` con los valores por defecto si no existe y carga tres usuarios de prueba (`admin`, `user_com`, `user_ware`) definidos en `scripts/seed_users.py`. **Son solo para desarrollo local**: cambia sus credenciales antes de desplegar en cualquier otro entorno.

> **Cambios en el esquema:** las tablas se crean con `create_all`, que no modifica tablas existentes. Tras cambiar un modelo, recrea la base de datos con `docker compose down -v` (borra todos los datos).

### Demostración del buzón seguro RSA

`scripts/send_secure_message.py` es un cliente independiente: descarga la clave pública, cifra un mensaje en local y lo envía a la API, que lo descifra con su clave privada.

```bash
docker compose exec -e NEXSALE_URL=http://apache nexsale_api python scripts/send_secure_message.py "HR1210010051863000160"
```

## Resumen de la API

| Método | Endpoint | Roles |
|---|---|---|
| `POST` | `/auth/login` | público |
| `GET` | `/auth/me` | cualquier usuario autenticado |
| `GET` / `POST` | `/users` | admin |
| `PUT` / `DELETE` | `/users/{id}` | admin |
| `GET` | `/products?order_by=&sort_order=&category=` | todos |
| `POST` | `/products` | admin, warehouse |
| `PUT` / `DELETE` | `/products/{id}` | admin, warehouse |
| `PUT` / `GET` | `/products/{id}/image` | admin, warehouse / todos |
| `GET` | `/orders?order_by=&sort_order=&customer=` | todos (los comerciales solo ven los suyos) |
| `POST` | `/orders` | admin, commercial |
| `PUT` | `/orders/{id}` | admin, commercial (sus pedidos) |
| `DELETE` | `/orders/{id}` | admin |
| `GET` | `/orders/{id}/report?format=pdf\|rtf` | público (ver [Próximos pasos](#próximos-pasos)) |
| `POST` | `/catalog/json/export` | admin, warehouse |
| `GET` | `/catalog/json` | todos |
| `PUT` / `DELETE` | `/catalog/json/{sku}` | admin, warehouse |
| `GET` / `PUT` | `/settings` | admin |
| `GET` | `/security/public-key` | público |
| `POST` | `/security/decrypt` | admin |
| `POST` | `/security/verify` (multipart: `file`, `signature`) | cualquier usuario autenticado |
| `GET` | `/health` | público |

## Próximos pasos

- [x] Firma digital de las facturas (RSA-PSS) y endpoint de verificación
- [ ] Versión XML de la tarifa de precios exportable
- [ ] Exigir autenticación para descargar facturas
- [ ] Fuente Unicode en las facturas (nombres de empresa con č, ć, š, ž, đ)
- [ ] Tests automáticos
- [ ] Migraciones de base de datos (Alembic)

## Autor

**Eneko Rodríguez** · [GitHub](https://github.com/enekorodriguezg)