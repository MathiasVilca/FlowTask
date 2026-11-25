from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.category import Category


class CategoryRepository:
    def __init__(self,db:Session)->None:
        self.db=db

    def get_all(self)->list[Category]:
        stmt=select(Category).order_by(Category.id.asc())
        return self.db.scalars(stmt).all()

    def get_by_id(self,category_id:int) -> Category|None:
        return self.db.get(Category,category_id)