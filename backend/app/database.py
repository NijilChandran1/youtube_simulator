from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings
import os

# Ensure directory exists for SQLite
db_path = settings.DATABASE_URL.replace("sqlite:///", "")
if db_path and "memory" not in db_path:
    # Handle relative paths properly
    if not os.path.isabs(db_path):
        # If running from root, path is relative to root
        base_dir = os.path.dirname(db_path)
    else:
        base_dir = os.path.dirname(db_path)
        
    if base_dir:
        os.makedirs(base_dir, exist_ok=True)

engine = create_engine(
    settings.DATABASE_URL, 
    connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
