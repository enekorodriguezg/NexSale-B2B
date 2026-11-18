# NexSale-B2B

[English](README.md) · **Español**

> 🚧 **Proyecto en desarrollo.** La autenticación y los flujos principales de productos y pedidos ya funcionan; algunos endpoints aún están en construcción (ver [Próximos pasos](#próximos-pasos)).

Backend transaccional para la gestión de pedidos y ventas entre empresas (B2B). Es una API REST construida con **FastAPI** que gestiona usuarios con distintos roles, un catálogo de productos con control de stock, pedidos de clientes y generación de facturas, todo desplegado con **Docker Compose** detrás de **Apache** como proxy inverso.

Desarrollado para la asignatura *Advanced Programming Techniques*.

## Funcionalidades

- **Autenticación con JWT** (flujo OAuth2 por contraseña) con sesiones de 8 horas.
- **Control de acceso por roles**, con tres roles:

  | Rol | Permisos |
  |---|---|
  | `admin` | Todo, incluido eliminar pedidos |
  | `commercial` | Crear pedidos y consultar el catálogo |
  | `warehouse` | Gestionar productos, stock e imágenes de producto |

- **Catálogo de productos**: alta de productos, listado ordenable, subida y descarga de imágenes.
- **Pedidos**: pedidos con varias líneas, comprobación y descuento automático de stock, cálculo del total y validación del identificador fiscal del cliente (OIB croata).
- **Facturas**: descarga de cualquier pedido como factura en **PDF** o **RTF**. La generación concurrente de informes está limitada con un semáforo.
- **Almacenamiento de contraseñas** con sal individual por usuario y *pepper* global.
- **Portal web**: frontend HTML ligero (inicio de sesión y gestión de pedidos) servido por Apache.
- **Documentación interactiva de la API** generada por FastAPI en `/docs` y `/redoc`.

## Tecnologías

| Capa | Tecnología |
|---|---|
| API | Python 3.11, FastAPI, Pydantic, Uvicorn |
| Persistencia | SQLAlchemy 2, MySQL 8 (PyMySQL) |
| Seguridad | PyJWT, hash de contraseñas con sal y *pepper* |
| Informes | fpdf2 (PDF), RTF |
| Infraestructura | Docker, Docker Compose, Apache httpd 2.4 (proxy inverso) |

## Arquitectura

```text
              ┌──────────────────────────── nexsale_net ────────────────────────────┐
 Navegador ──►│  Apache :80  ──(/auth, /products, /orders, /docs)──►  FastAPI :8000 │
              │     │                                                    │          │
              │     └── sirve frontend/index.html                        ▼          │
              │                                                     MySQL :3306     │
              └─────────────────────────────────────────────────────────────────────┘
```

El código está organizado por capas:

```text
server/
├── main.py          Punto de entrada y registro de routers
├── routers/         Endpoints HTTP (auth, products, orders)
├── services/        Lógica de negocio (pedidos, stock, informes, auth)
├── schemas/         Modelos Pydantic de validación y respuesta
├── models.py        Modelos ORM de SQLAlchemy
├── api/deps.py      Dependencias: usuario actual, RoleChecker
└── core/            Configuración y seguridad (hash, JWT)
frontend/            Portal web estático
apache/              Imagen y virtual host del proxy inverso
scripts/             Carga inicial de la base de datos
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
   | `MYSQL_PORT` | Puerto del host en el que se expone MySQL |
   | `PEPPER` | Secreto que se añade a todas las contraseñas antes del hash |
   | `SECRET_KEY` | Clave con la que se firman los JWT |

3. Construye y arranca los servicios:

   ```bash
   docker compose up --build
   ```

4. Abre:
   - Portal web: <http://localhost>
   - Documentación de la API: <http://localhost/docs>

Al arrancar, la API crea las tablas y carga tres usuarios de prueba (`admin`, `user_com`, `user_ware`) definidos en `scripts/seed_users.py`. **Son solo para desarrollo local**: cambia sus credenciales antes de desplegar en cualquier otro entorno.

## Resumen de la API

| Método | Endpoint | Roles |
|---|---|---|
| `POST` | `/auth/login` | público |
| `GET` | `/auth/me` | cualquier usuario autenticado |
| `GET` | `/products` | todos |
| `POST` | `/products` | admin, warehouse |
| `PUT` / `GET` | `/products/{id}/image` | admin, warehouse / todos |
| `POST` | `/orders` | admin, commercial |
| `GET` | `/orders` | todos |
| `DELETE` | `/orders/{id}` | admin |
| `GET` | `/orders/{id}/report?format=pdf\|rtf` | público (ver [Próximos pasos](#próximos-pasos)) |
| `GET` | `/health` | público |

## Próximos pasos

- [ ] Modificar pedidos (`PUT /orders`)
- [ ] Modificar y eliminar productos (`PUT` / `DELETE /products/{id}`)
- [ ] Exigir autenticación para descargar facturas
- [ ] Cambiar el hash de contraseñas a un algoritmo específico (Argon2 / bcrypt)
- [ ] Tests automáticos
- [ ] Migraciones de base de datos (Alembic)

## Autor

**Eneko Rodríguez** · [GitHub](https://github.com/enekorodriguezg)
