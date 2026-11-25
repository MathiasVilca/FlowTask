from app.repositories.category_repository import CategoryRepository
from app.models.category import Category
from sqlalchemy.orm import Session

class CategoryService:
    def __init__(self,db : Session) -> None:
        self.repository=CategoryRepository(db)

    def list_categories(self) -> list[Category]:
        return self.repository.get_all()