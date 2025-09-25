# app/db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import redis
from config import DATABASE_URL, REDIS_URL

# SQLAlchemy
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()

redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)

def check_redis():
    """
    Comprueba si Redis está conectado.
    """
    try:
        redis_client.ping()
        print("✅ Redis conectado correctamente")
    except Exception as e:
        print("❌ Error al conectar Redis:", e)