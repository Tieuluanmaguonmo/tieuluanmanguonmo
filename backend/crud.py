from sqlalchemy.orm import Session
from datetime import date
from uuid import UUID

from models import NguoiDung, BoFlashcard, Flashcard, TienDoHoc
from security import hash_mat_khau, verify_mat_khau

# ==================================================
# NGƯỜI DÙNG
# ==================================================

# CREATE
def tao_nguoi_dung(db: Session, email: str, mat_khau: str):
    if db.query(NguoiDung).filter(NguoiDung.email == email).first():
        return None
    nguoi_dung = NguoiDung(
        email=email,
        mat_khau_hash=hash_mat_khau(mat_khau)
    )
    db.add(nguoi_dung)
    db.commit()
    db.refresh(nguoi_dung)
    return nguoi_dung

# READ
def cap_nhat_mat_khau(db: Session, nguoi_dung_id: UUID, mat_khau_moi: str):
    nd = db.query(NguoiDung).filter(NguoiDung.id == nguoi_dung_id).first()
    if not nd:
        return None
    nd.mat_khau_hash = mat_khau_moi  # Lưu trực tiếp hoặc hash trước khi lưu
    db.commit()
    db.refresh(nd)
    return nd

def lay_nguoi_dung_theo_id(db: Session, nguoi_dung_id: UUID):
    return db.query(NguoiDung).filter(NguoiDung.id == nguoi_dung_id).first()

def lay_nguoi_dung_theo_email(db: Session, email: str):
    return db.query(NguoiDung).filter(NguoiDung.email == email).first()

def lay_tat_ca_nguoi_dung(db: Session):
    return db.query(NguoiDung).all()

# UPDATE
def cap_nhat_nguoi_dung(db: Session, nguoi_dung_id: UUID, **kwargs):
    nguoi_dung = lay_nguoi_dung_theo_id(db, nguoi_dung_id)
    if not nguoi_dung:
        return None
    for key, value in kwargs.items():
        setattr(nguoi_dung, key, value)
    db.commit()
    db.refresh(nguoi_dung)
    return nguoi_dung

# DELETE
def xoa_nguoi_dung(db: Session, nguoi_dung_id: UUID):
    nguoi_dung = lay_nguoi_dung_theo_id(db, nguoi_dung_id)
    if not nguoi_dung:
        return False
    db.delete(nguoi_dung)
    db.commit()
    return True

# AUTH
def xac_thuc_nguoi_dung(db: Session, email: str, mat_khau: str):
    nguoi_dung = lay_nguoi_dung_theo_email(db, email)
    if not nguoi_dung or not verify_mat_khau(mat_khau, nguoi_dung.mat_khau_hash):
        return None
    return nguoi_dung

# ==================================================
# BỘ FLASHCARD
# ==================================================

# CREATE
def tao_bo_flashcard(db: Session, nguoi_dung_id: UUID, ten: str, mo_ta: str | None = None):
    bo = BoFlashcard(nguoi_dung_id=nguoi_dung_id, ten=ten, mo_ta=mo_ta)
    db.add(bo)
    db.commit()
    db.refresh(bo)
    return bo

# READ
def lay_bo_flashcard_theo_id(db: Session, bo_id: UUID):
    return db.query(BoFlashcard).filter(BoFlashcard.id == bo_id).first()

def lay_danh_sach_bo_flashcard(db: Session, nguoi_dung_id: UUID):
    return db.query(BoFlashcard).filter(BoFlashcard.nguoi_dung_id == nguoi_dung_id).all()

def lay_tat_ca_bo_flashcard(db: Session):
    return db.query(BoFlashcard).all()

# UPDATE
def cap_nhat_bo_flashcard(db: Session, bo_id: UUID, ten: str | None = None, mo_ta: str | None = None):
    bo = lay_bo_flashcard_theo_id(db, bo_id)
    if not bo:
        return None
    if ten is not None:
        bo.ten = ten
    if mo_ta is not None:
        bo.mo_ta = mo_ta
    db.commit()
    db.refresh(bo)
    return bo

# DELETE
def xoa_bo_flashcard(db: Session, bo_id: UUID):
    bo = lay_bo_flashcard_theo_id(db, bo_id)
    if not bo:
        return False
    db.delete(bo)
    db.commit()
    return True

# ==================================================
# FLASHCARD
# ==================================================

# CREATE
def tao_flashcard(db: Session, bo_id: UUID, mat_truoc: str, mat_sau: str, vi_du: str | None = None):
    fc = Flashcard(bo_flashcard_id=bo_id, mat_truoc=mat_truoc, mat_sau=mat_sau, vi_du=vi_du)
    db.add(fc)
    db.commit()
    db.refresh(fc)
    return fc

# READ
def lay_flashcard_theo_id(db: Session, flashcard_id: UUID):
    return db.query(Flashcard).filter(Flashcard.id == flashcard_id).first()

def lay_flashcard_theo_bo(db: Session, bo_id: UUID):
    return db.query(Flashcard).filter(Flashcard.bo_flashcard_id == bo_id).all()

def lay_tat_ca_flashcard(db: Session):
    return db.query(Flashcard).all()

# UPDATE
def cap_nhat_flashcard(db: Session, flashcard_id: UUID, mat_truoc: str | None = None, mat_sau: str | None = None, vi_du: str | None = None):
    fc = lay_flashcard_theo_id(db, flashcard_id)
    if not fc:
        return None
    if mat_truoc is not None:
        fc.mat_truoc = mat_truoc
    if mat_sau is not None:
        fc.mat_sau = mat_sau
    if vi_du is not None:
        fc.vi_du = vi_du
    db.commit()
    db.refresh(fc)
    return fc

# DELETE
def xoa_flashcard(db: Session, flashcard_id: UUID):
    fc = lay_flashcard_theo_id(db, flashcard_id)
    if not fc:
        return False
    db.delete(fc)
    db.commit()
    return True

# ==================================================
# TIẾN ĐỘ HỌC (SPACED REPETITION)
# ==================================================

# CREATE
def tao_tien_do_hoc(db: Session, nguoi_dung_id: UUID, flashcard_id: UUID, ngay_on_tiep: date):
    tien_do = TienDoHoc(nguoi_dung_id=nguoi_dung_id, flashcard_id=flashcard_id, ngay_on_tiep=ngay_on_tiep)
    db.add(tien_do)
    db.commit()
    db.refresh(tien_do)
    return tien_do

# READ
def lay_flashcard_can_on(db: Session, nguoi_dung_id: UUID):
    return db.query(TienDoHoc).filter(
        TienDoHoc.nguoi_dung_id == nguoi_dung_id,
        TienDoHoc.ngay_on_tiep <= date.today()
    ).all()

def lay_tien_do_theo_flashcard(db: Session, flashcard_id: UUID):
    return db.query(TienDoHoc).filter(TienDoHoc.flashcard_id == flashcard_id).first()

# UPDATE
def cap_nhat_ngay_on(db: Session, tien_do_id: UUID, ngay_on_moi: date):
    tien_do = db.query(TienDoHoc).filter(TienDoHoc.id == tien_do_id).first()
    if not tien_do:
        return None
    tien_do.ngay_on_tiep = ngay_on_moi
    db.commit()
    db.refresh(tien_do)
    return tien_do

# DELETE
def xoa_tien_do_hoc(db: Session, tien_do_id: UUID):
    tien_do = db.query(TienDoHoc).filter(TienDoHoc.id == tien_do_id).first()
    if not tien_do:
        return False
    db.delete(tien_do)
    db.commit()
    return True
