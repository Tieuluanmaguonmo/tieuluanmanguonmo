from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime, date
from uuid import UUID

# =====================
# NGƯỜI DÙNG
# =====================
class TaoNguoiDung(BaseModel):
    email: EmailStr
    mat_khau: str


class DangNhap(BaseModel):
    email: EmailStr
    mat_khau: str


class NguoiDungOut(BaseModel):
    id: UUID
    email: EmailStr
    ngay_tao: datetime

    class Config:
        from_attributes = True


# =====================
# BỘ FLASHCARD
# =====================
class TaoBoFlashcard(BaseModel):
    ten: str
    mo_ta: Optional[str] = None


class CapNhatBoFlashcard(BaseModel):
    ten: Optional[str] = None
    mo_ta: Optional[str] = None


class BoFlashcardOut(BaseModel):
    id: UUID
    ten: str
    mo_ta: Optional[str]
    nguoi_dung_id: UUID

    class Config:
        from_attributes = True


# =====================
# FLASHCARD
# =====================
class TaoFlashcard(BaseModel):
    mat_truoc: str
    mat_sau: str
    vi_du: Optional[str] = None


class CapNhatFlashcard(BaseModel):
    mat_truoc: Optional[str] = None
    mat_sau: Optional[str] = None
    vi_du: Optional[str] = None


class FlashcardOut(BaseModel):
    id: UUID
    mat_truoc: str
    mat_sau: str
    vi_du: Optional[str]
    bo_flashcard_id: UUID

    class Config:
        from_attributes = True


# =====================
# HỌC / SPACED REPETITION
# =====================
class DanhGiaHoc(BaseModel):
    muc_do: str  # "de", "binh_thuong", "kho"


class TienDoHocOut(BaseModel):
    id: UUID
    nguoi_dung_id: UUID
    flashcard_id: UUID
    so_lan_on: int
    khoang_cach_ngay: int
    he_so_de: float
    ngay_on_tiep: date
    lan_on_cuoi: Optional[date]

    class Config:
        from_attributes = True
