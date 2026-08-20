from sqlalchemy import text
from utils.db.database import engine

with engine.begin() as conn:
    conn.execute(text(
        "ALTER TABLE users ADD COLUMN display_name VARCHAR"
    ))

print("display_name added")