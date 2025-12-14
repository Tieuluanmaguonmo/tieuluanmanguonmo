import uuid
from sqlalchemy import Column, String, Text, Integer, Float, Date, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

# ========================
# NGƯỜI DÙNG
# ========================
class NguoiDung(Base):
    __tablename__ = "nguoi_dung"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    mat_khau_hash = Column(Text, nullable=False)
    ngay_tao = Column(DateTime, server_default=func.now())

    # Quan hệ
    bo_flashcards = relationship("BoFlashcard", back_populates="nguoi_dung", cascade="all, delete-orphan")
    tien_do_hoc = relationship("TienDoHoc", back_populates="nguoi_dung", cascade="all, delete-orphan")


# ========================
# BỘ FLASHCARD
# ========================
class BoFlashcard(Base):
    __tablename__ = "bo_flashcard"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nguoi_dung_id = Column(PG_UUID(as_uuid=True), ForeignKey("nguoi_dung.id"), nullable=False)

    ten = Column(String, nullable=False)
    mo_ta = Column(Text)
    ngay_tao = Column(DateTime, server_default=func.now())

    # Quan hệ
    nguoi_dung = relationship("NguoiDung", back_populates="bo_flashcards")
    flashcards = relationship("Flashcard", back_populates="bo_flashcard", cascade="all, delete-orphan")


# ========================
# FLASHCARD
# ========================
class Flashcard(Base):
    __tablename__ = "flashcard"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    bo_flashcard_id = Column(PG_UUID(as_uuid=True), ForeignKey("bo_flashcard.id"), nullable=False)

    mat_truoc = Column(Text, nullable=False)
    mat_sau = Column(Text, nullable=False)
    vi_du = Column(Text)
    ngay_tao = Column(DateTime, server_default=func.now())

    # Quan hệ
    bo_flashcard = relationship("BoFlashcard", back_populates="flashcards")
    tien_do_hoc = relationship("TienDoHoc", back_populates="flashcard", cascade="all, delete-orphan")


# ========================
# TIẾN ĐỘ HỌC
# ========================
class TienDoHoc(Base):
    __tablename__ = "tien_do_hoc"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nguoi_dung_id = Column(PG_UUID(as_uuid=True), ForeignKey("nguoi_dung.id"), nullable=False)
    flashcard_id = Column(PG_UUID(as_uuid=True), ForeignKey("flashcard.id"), nullable=False)

    so_lan_on = Column(Integer, default=0)
    khoang_cach_ngay = Column(Integer, default=1)
    he_so_de = Column(Float, default=2.5)
    ngay_on_tiep = Column(Date)
    lan_on_cuoi = Column(Date)

    # Quan hệ
    nguoi_dung = relationship("NguoiDung", back_populates="tien_do_hoc")
    flashcard = relationship("Flashcard", back_populates="tien_do_hoc")
