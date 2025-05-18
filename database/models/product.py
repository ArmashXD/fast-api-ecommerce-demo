from sqlalchemy import Column, Integer, String, Float, DateTime, func
from sqlalchemy.orm import relationship
from database.connection import Base

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    category = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    sales = relationship("Sale", back_populates="product")
    inventories = relationship("Inventory", back_populates="product")
