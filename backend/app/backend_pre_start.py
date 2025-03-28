import logging
from sqlalchemy import create_engine, text
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main() -> None:
    logger.info("Checking database connection...")
    POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_SERVER = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
    POSTGRES_DB = os.getenv("POSTGRES_DB", "app")
    
    database_url = f"postgresql+psycopg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
    
    try:
        engine = create_engine(database_url)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("Database is ready")
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        raise e

if __name__ == "__main__":
    main()
