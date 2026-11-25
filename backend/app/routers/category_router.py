from fastapi import APIRouter,Depends
from typing import Annotated
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.category import CategoryResponse
from app.services.category_service import CategoryService

router=APIRouter(prefix="/categories",tags=["Categorías"])
DbSession = Annotated[Session, Depends(get_db)]

@router.get(
        "",
        response_model=list[CategoryResponse],
        status_code=200,
        summary="Listar categorías",
        description="Devuelve todas las categorías disponibles en la base de datos"
        )
def get_categories(description):
    service=CategoryService(DbSession)
    return service.list_categories()


    
