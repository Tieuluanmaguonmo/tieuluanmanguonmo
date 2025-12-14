from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# =====================
# DATABASE CONFIG
# =====================
DATABASE_URL = "postgresql://student:yQrceD9FL3y4q74Ks6s4fXGJYSwDPI8A@dpg-d4v6j0er433s73dvqu6g-a.virginia-postgres.render.com:5432/flashcard_82o8"

# =====================
# ENGINE
# =====================
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,   # tự động reconnect nếu mất kết nối
)

# =====================
# SESSION
# =====================
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# =====================
# BASE MODEL
# =====================
Base = declarative_base()
