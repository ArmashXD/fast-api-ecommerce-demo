from database.connection import SessionLocal
from database.models.product import Product
from database.models.inventory import Inventory
from database.models.sale import Sale
from datetime import datetime, timedelta
import random

def populate_demo_data():
    db = SessionLocal()
    try:
        products = [
            Product(name="Amazon Echo", category="Electronics", price=99.99),
            Product(name="Walmart T-Shirt", category="Clothing", price=15.99),
            Product(name="Amazon Kindle", category="Electronics", price=79.99),
            Product(name="Walmart Sneakers", category="Footwear", price=49.99),
        ]
        db.add_all(products)
        db.commit()
        print("Inserted sample products.")

        inventories = []
        for product in products:
            inv = Inventory(product_id=product.id, quantity=random.randint(20, 100))
            inventories.append(inv)
        db.add_all(inventories)
        db.commit()
        print("Inserted sample inventories.")

        sales = []
        start_date = datetime.now() - timedelta(days=30)
        for product in products:
            for _ in range(random.randint(5, 15)):
                sale_date = start_date + timedelta(days=random.randint(0, 29))
                quantity = random.randint(1, 5)
                total_price = product.price * quantity
                sale = Sale(
                    product_id=product.id,
                    quantity=quantity,
                    sale_date=sale_date,
                    total_price=total_price,
                )
                sales.append(sale)
        db.add_all(sales)
        db.commit()
        print("Inserted sample sales.")
    finally:
        db.close()

if __name__ == "__main__":
    populate_demo_data()
