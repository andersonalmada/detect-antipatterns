# observa/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

# Carrega variáveis do arquivo .env (se existir)
load_dotenv()

# Lê as variáveis de ambiente do Postgres
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB", "observa_db")

# Monta a URL final (ou usa DATABASE_URL diretamente, se definida)
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

# Cria o engine SQLAlchemy
engine = create_engine(DATABASE_URL, echo=False, future=True)

# Cria o factory para sessões
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)

# Base para os modelos ORM
Base = declarative_base()
