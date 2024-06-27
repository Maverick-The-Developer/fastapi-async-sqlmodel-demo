from typing import Optional
from sqlmodel import Field, SQLModel

class Product(SQLModel, table=True):
    __tablename__ = "product"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str] = ""
    description: Optional[str] = ""
    price: Optional[ float ] = 0.0
    stock: Optional[ int ] = 0
