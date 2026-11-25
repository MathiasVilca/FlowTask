from app.core.database import Base, SessionLocal, engine
from app.models.category import Category

DEFAULT_CATEGORIES=[
    {
        "name": "Trabajo",
        "description":"Tareas laborales, reuniones."
    },
    {
        "name": "Estudio",
        "description":"Cursos y especializaciones."
    },
    {
        "name": "Personal",
        "description":"Cuidado personal, salud."
    },
    {
        "name": "Hogar",
        "description":"Compras, mantenimiento y cuidado del hogar."
    },
]

def seeding() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        inserted=0
        for item in DEFAULT_CATEGORIES:
            is_Category= (
                db.query(Category)
                .filter(Category.name==item["name"])
                .first()
            )

            if not is_Category:
                db.add(Category(**item))
                inserted+=1
        db.commit()
        print(f"Seeding completado: Se insertaron {inserted} categorías")
    except Exception as exc:
        db.rollback()
        print(f"Ocurrió un error: {exc}")
    finally:
        db.close()

if __name__ == "__main__":
    seeding()