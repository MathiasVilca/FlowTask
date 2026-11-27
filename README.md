# FlowTask — Gestor de Tareas por Categorías

Aplicación web *fullstack* para la gestión de tareas (CRUD completo), con filtrado combinado por estado y categoría, acciones rápidas de completado/eliminación y validación tanto en cliente como en servidor.

## Stack Tecnológico

* **Backend:** Python 3.11+, FastAPI, SQLAlchemy, Pydantic, SQLite.
* **Frontend:** Angular (componentes *standalone*), TypeScript, RxJS, Tailwind CSS.
* **Calidad de código:** Black, Flake8, ESLint y Prettier.

---

## Requisitos Previos

* **Python:** 3.11 o superior
* **Node.js:** 20.x o 24.x (LTS)
* **Angular CLI:** 19+ (`npm install -g @angular/cli`)
* **Git**

---

## Estructura del Proyecto

```text
FlowTask/
├── backend/                # API REST con FastAPI y SQLite
│   ├── app/
│   │   ├── core/           # Configuración de BD y Enums
│   │   ├── models/         # Modelos ORM (SQLAlchemy)
│   │   ├── schemas/        # Esquemas de validación (Pydantic)
│   │   ├── repositories/   # Acceso a datos
│   │   ├── services/       # Lógica de negocio
│   │   ├── routers/        # Endpoints REST (/tasks, /categories)
│   │   └── main.py         # Punto de entrada y configuración CORS
│   ├── requirements.txt
│   └── seed.py             # Script idempotente de categorías iniciales
├── frontend/               # SPA con Angular y Tailwind CSS
│   └── src/
│       ├── environments/   # URL base de la API
│       └── app/
│           ├── models/     # Interfaces y tipos TypeScript
│           ├── services/   # Servicios HTTP y estado reactivo (RxJS)
│           └── components/ # TaskList, TaskCard y TaskForm
└── README.md
```

---

## Instalación y Ejecución del Backend

1. **Entrar a la carpeta del backend y crear el entorno virtual:**
   ```bash
   cd backend
   python -m venv venv
   ```

2. **Activar el entorno virtual:**
   * En Linux/macOS:
     ```bash
     source venv/bin/activate
     ```
   * En Windows:
     ```bash
     venv\Scripts\activate
     ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecutar el script de semilla (crea la base de datos SQLite y las categorías iniciales):**
   ```bash
   python seed.py
   ```

5. **Levantar el servidor de desarrollo:**
   ```bash
   uvicorn app.main:app --reload
   ```
   * **API disponible en:** `http://localhost:8000`
   * **Documentación interactiva (Swagger UI):** `http://localhost:8000/docs`

---

## Instalación y Ejecución del Frontend

En una segunda terminal, desde la raíz del proyecto:

1. **Entrar a la carpeta del frontend e instalar paquetes:**
   ```bash
   cd frontend
   npm install
   ```

2. **Levantar el servidor de desarrollo:**
   ```bash
   ng serve
   ```
   * **Aplicación disponible en:** `http://localhost:4200`

## (EXTRA) Ejecución Rápida con Docker

Si tienes **Docker** y **Docker Compose** instalados, puedes construir y levantar tanto el backend (con las categorías iniciales precargadas de `seed.py`) como el frontend en un solo comando desde la raíz del proyecto:

1. **Construir y levantar los contenedores:**
   ```bash
   docker compose up --build -d

2. **Acceder a la aplicación:**
   * **Frontend (Angular + Nginx):** `http://localhost:4200`
   * **Backend API (FastAPI):** `http://localhost:8000`
   * **Documentación Swagger:** `http://localhost:8000/docs`

3. **Detener los contenedores:**
   ```bash
   docker compose down
   ```
   *(Si deseas eliminar también el volumen de la base de datos, ejecuta `docker compose down -v`).*

---

## Decisiones Técnicas y Patrones Utilizados

### Backend (FastAPI)
* **Arquitectura en Capas (`Routers → Services → Repositories`):** Se separaron en 3 niveles: Routers (Rutas HTTP), Services (Lógica de negocio) y Repositories (Acceso a datos), esto para evitar consultas SQL dentro de los controladores, facilitar el mantenimiento y reutilizar reglas (como validar que una categoría exista antes de crear o actualizar una tarea).
* **Separación entre Modelos ORM y Schemas Pydantic:** Los modelos de `models/` representan las tablas en SQLite, mientras que `schemas/` controla estrictamente la validación de entrada (`TaskCreate`, `TaskUpdate`), rechaza títulos compuestos solo por espacios en blanco y serializa relaciones anidadas (`TaskResponse` con `CategoryResponse`) para evitar peticiones extra desde el frontend.
* **Inyección de Dependencias (`Depends(get_db)`):** FastAPI inyecta automáticamente una sesión de base de datos aislada en cada petición HTTP y garantiza su cierre al terminar, evitando bloqueos o fugas en SQLite.
* **Seeding Idempotente (`seed.py`):** Verifica la existencia previa de cada categoría antes de insertarla, permitiendo ejecutar el script múltiples veces sin duplicar registros. Se ejecuta al levantar la app con Docker.

### Frontend (Angular)
* **Componentización (*Smart & Presentational*):** `TaskList` actúa como componente contenedor encargado de coordinar filtros, modal y llamadas al servicio; `TaskCard` y `TaskForm` son componentes reutilizables desacoplados que reciben datos por `input()` y emiten eventos por `output()`.
* **Estado Reactivo con RxJS (`BehaviorSubject`):** `TaskService` centraliza el listado de tareas en memoria y lo actualiza automáticamente tras alguna acción que las modifique (crear, editar, completar o eliminar una tarea), reflejando los cambios sin necesidad de recargar la página.
* **Formularios Reactivos (`ReactiveFormsModule`):** `TaskForm` reutiliza el mismo formulario para creación (`POST`) y edición (`PATCH/PUT`), sincronizando los datos mediante Angular Signals (`effect()`), distinguiendo entre tareas dependiendo si el parámetro `Task` es `null` y validando campos obligatorios antes del envío.