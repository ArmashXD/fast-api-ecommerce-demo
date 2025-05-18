from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from typing import List, Optional
from datetime import datetime, date
from pydantic import BaseModel

from database.connection import SessionLocal
from database.models.sale import Sale
from database.models.product import Product

router = APIRouter()

class SaleOut(BaseModel):
    id: int
    product_id: int
    quantity: int
    sale_date: datetime
    total_price: float

    class Config:
        orm_mode = True

class RevenueOut(BaseModel):
    period: str
    total_revenue: float

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[SaleOut])
def get_sales(
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    product_id: Optional[int] = Query(None),
    category: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(Sale).join(Product)

    if start_date:
        query = query.filter(Sale.sale_date >= datetime.combine(start_date, datetime.min.time()))
    if end_date:
        query = query.filter(Sale.sale_date <= datetime.combine(end_date, datetime.max.time()))
    if product_id:
        query = query.filter(Sale.product_id == product_id)
    if category:
        query = query.filter(Product.category == category)

    return query.all()

@router.get("/revenue/", response_model=List[RevenueOut])
def get_revenue(
    period: str = Query("daily", regex="^(daily|weekly|monthly|annually)$"),
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    category: Optional[str] = None,
    db: Session = Depends(get_db),
):
    base_query = db.query(func.sum(Sale.total_price).label("total_revenue")).join(Product)

    if start_date:
        base_query = base_query.filter(Sale.sale_date >= datetime.combine(start_date, datetime.min.time()))
    if end_date:
        base_query = base_query.filter(Sale.sale_date <= datetime.combine(end_date, datetime.max.time()))

    if category:
        base_query = base_query.filter(Product.category == category)

    if period == "daily":
        base_query = base_query.add_columns(func.date(Sale.sale_date).label("period"))\
            .group_by(func.date(Sale.sale_date))\
            .order_by(func.date(Sale.sale_date))
    elif period == "weekly":
        base_query = base_query.add_columns(
            extract('year', Sale.sale_date).label("year"),
            extract('week', Sale.sale_date).label("week")
        ).group_by("year", "week").order_by("year", "week")
    elif period == "monthly":
        base_query = base_query.add_columns(
            extract('year', Sale.sale_date).label("year"),
            extract('month', Sale.sale_date).label("month")
        ).group_by("year", "month").order_by("year", "month")
    else:  # annually
        base_query = base_query.add_columns(
            extract('year', Sale.sale_date).label("year")
        ).group_by("year").order_by("year")

    results = base_query.all()

    revenue_list = []
    for row in results:
        revenue = row[0]
        if period == "daily":
            period_val = row[1].isoformat()
        elif period == "weekly":
            period_val = f"{int(row[1])}-W{int(row[2])}"
        elif period == "monthly":
            period_val = f"{int(row[1])}-{int(row[2]):02d}"
        else:
            period_val = str(int(row[1]))

        revenue_list.append({"period": period_val, "total_revenue": float(revenue)})

    return revenue_list
