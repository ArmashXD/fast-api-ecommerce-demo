
from fastapi import FastAPI 
from sqlalchemy.orm import Session

from database.connection import SessionLocal, engine, Base
from database.models import Product, Sale, Inventory

from routers import products_router, sales_router, revenue_router, inventory_router

app = FastAPI(title="E-commerce API")

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(products_router, prefix="/products", tags=["Products"])
app.include_router(sales_router, prefix="/sales", tags=["Sales"])
app.include_router(revenue_router, prefix="/revenue", tags=["Revenue"])
app.include_router(inventory_router, prefix="/inventory", tags=["Inventory"])

@app.get('/')
def read_root():
    return {"Hello": "World"}
