from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from database.connection import SessionLocal
from database.models.inventory import Inventory

router = APIRouter()

class InventoryOut(BaseModel):
    product_id: int
    quantity: int

    class Config:
        orm_mode = True

  

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[InventoryOut])
def get_inventory(low_stock_threshold: Optional[int] = Query(None, ge=0), db: Session = Depends(get_db)):
    query = db.query(Inventory)
    if low_stock_threshold is not None:
        query = query.filter(Inventory.quantity <= low_stock_threshold)
    return query.all()

@router.put("/{product_id}/", response_model=InventoryOut)
def update_inventory(product_id: int, quantity: int = Query(..., ge=0), db: Session = Depends(get_db)):
    inventory = db.query(Inventory).filter(Inventory.product_id == product_id).first()
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory not found")
    inventory.quantity = quantity
    db.commit()
    db.refresh(inventory)
    return inventory
