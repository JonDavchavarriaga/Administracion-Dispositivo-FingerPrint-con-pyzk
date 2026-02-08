from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "huellero_db")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


def init_db():
    """
    Inicializa la base de datos ejecutando el schema.sql
    NO crea tablas con SQLAlchemy
    """
    schema_path = Path(
        "src/infrastructure/repositories/mysql/schema.sql"
    )

    if not schema_path.exists():
        raise FileNotFoundError("schema.sql no encontrado")

    with engine.connect() as connection:
        sql = schema_path.read_text(encoding="utf-8")
        for statement in sql.split(";"):
            if statement.strip():
                connection.execute(text(statement))
        connection.commit()
