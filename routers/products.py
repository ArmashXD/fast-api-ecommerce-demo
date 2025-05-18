from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel

from database.connection import SessionLocal
from database.models.product import Product

router = APIRouter()

class ProductCreate(BaseModel):
    name: str
    category: str
    price: float

class ProductOut(BaseModel):
    id: int
    name: str
    category: str
    price: float

    class Config:
        orm_mode = True

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=ProductOut)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    exists = db.query(Product).filter(Product.name == product.name).first()
    if exists:
        raise HTTPException(status_code=400, detail="Product already exists")
    new_product = Product(**product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@router.get("/", response_model=List[ProductOut])
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()
