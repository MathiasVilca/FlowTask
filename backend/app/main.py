from app.core.database import Base, engine
from app.routers import category_router, task_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Flowtask", description="App de administración de tareas")

allowed_origins = {
    "http://localhost:4200",
    "http://127.0.0.1:4200",
    "http://localhost",
}

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"],
)

app.include_router(category_router.router)
app.include_router(task_router.router)
