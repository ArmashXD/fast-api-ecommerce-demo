# E-commerce API (FastAPI + SQLAlchemy + MySQL)

A simple FastAPI project that exposes CRUD endpoints for **Products**, **Sales**, **Revenue** and **Inventory** backed by a MySQL database.

---

## ⚡️ Quick start

```bash
# 1. Clone
git clone https://github.com/ArmashXD/fast-api-ecommerce-demo
cd fast-api-ecommerce-demo
```

# 1. Create & activate a virtual-env (any tool works)

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
```

# 2. Install Python deps

```bash
pip install -r requirements.txt
```

# 3. Configure environment variables

```bash
cp .env.example .env               # then edit .env

python migrate.py                  # creates the tables
python populate_demo.py            # fills with sample rows
```

# 4. Run the API

```bash
uvicorn main:app --reload
```

## 📂 Project layout

```bash
fast-api/
│
├── database/               ← SQLAlchemy models & DB connection
│   ├── connection.py
│   └── models/
│
├── routers/                ← FastAPI routers (blueprints)
│   ├── products_router.py
│   ├── sales_router.py
│   ├── revenue_router.py
│   └── inventory_router.py
│
├── main.py                 ← App entry-point
├── migrate.py              ← One-shot table-creator script
├── populate_demo.py        ← Optional sample-data loader
├── .env.example            ← Template for env vars
└── .gitignore
```

## 🛠 Configuration

```bash
DATABASE_URL=mysql+pymysql://<user>:<password>@<host>:<port>/<database>
```

## Endpoints

```bash

| Method | Path         | Purpose              |
| ------ | ------------ | -------------------- |
| GET    | `/products`  | List products        |
| POST   | `/products`  | Add product          |
| GET    | `/inventory` | Current stock levels |
| POST   | `/sales`     | Record a sale        |
| GET    | `/revenue`   | Revenue summary      |
```
