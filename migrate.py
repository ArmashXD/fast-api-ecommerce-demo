from database.connection import engine, Base
from database.models.product import Product
from database.models.sale import Sale
from database.models.inventory import Inventory

def run_migrations():
    print("Creating all tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")

if __name__ == "__main__":
    run_migrations()
