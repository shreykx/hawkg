from sqlalchemy import text
from utils.db.database import engine

with engine.begin() as conn:
    conn.execute(text(
        "ALTER TABLE users ADD COLUMN profile_image_version INTEGER NOT NULL DEFAULT 1"
    ))

print("profile_image_version added")