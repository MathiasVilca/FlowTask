from app.schemas.base import AppBaseModel
from pydantic import ConfigDict,Field
from typing import Optional

class CategoryBase(AppBaseModel):
    name: str = Field(...,min_length=1,max_length=50)
    description: Optional[str] = Field(None,max_length=100)

class CategoryResponse(CategoryBase):
    model_config=ConfigDict(from_attributes=True)
    id: int