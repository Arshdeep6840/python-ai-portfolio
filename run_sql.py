"""Small dev utility: run the query in lite.sql against the real app database.

Usage:
    python run_sql.py
"""
import os

from sqlalchemy import create_engine, text

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "instance", "portfolio.db")

# 1. Connect to the same SQLite database the Flask app uses (instance/portfolio.db)
engine = create_engine(f"sqlite:///{DB_PATH}")

# 2. Read the query from lite.sql
with open(os.path.join(BASE_DIR, "lite.sql"), "r") as file:
    sql_query = file.read()

# 3. Execute it
with engine.connect() as connection:
    result = connection.execute(text(sql_query))
    if result.returns_rows:
        for row in result:
            print(row)
