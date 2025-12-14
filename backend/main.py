from fastapi import Body, FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from uuid import UUID
from fastapi.middleware.cors import CORSMiddleware

from database import SessionLocal, engine
import models, schemas, crud
from spaced_repetition import cap_nhat_spaced_repetition

# =====================
# INIT DATABASE
# =====================
if __name__ == "__main__":
    models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Flashcard Study App")

# =====================
# CORS
# =====================
origins = [
    "http://127.0.0.1:5500",
    "http://localhost:5500",
    "http://127.0.0.1:5173",
    "http://localhost:5173",
    "https://tieuluanmanguonmo-4uxf.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================
# DATABASE DEPENDENCY
# =====================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# =====================
# NGƯỜI DÙNG (CRUD)
# =====================
@app.post("/nguoi-dung", response_model=schemas.NguoiDungOut)
def tao_nguoi_dung(data: schemas.TaoNguoiDung, db: Session = Depends(get_db)):
    nd = crud.tao_nguoi_dung(db, data.email, data.mat_khau)
    if not nd:
        raise HTTPException(status_code=400, detail="Email đã tồn tại")
    return nd

@app.get("/nguoi-dung", response_model=list[schemas.NguoiDungOut])
def lay_tat_ca_nguoi_dung(db: Session = Depends(get_db)):
    return crud.lay_tat_ca_nguoi_dung(db)

@app.get("/nguoi-dung/{nguoi_dung_id}", response_model=schemas.NguoiDungOut)
def lay_nguoi_dung(nguoi_dung_id: UUID, db: Session = Depends(get_db)):
    nd = crud.lay_nguoi_dung_theo_id(db, nguoi_dung_id)
    if not nd:
        raise HTTPException(status_code=404, detail="Không tìm thấy người dùng")
    return nd

@app.delete("/nguoi-dung/{nguoi_dung_id}")
def xoa_nguoi_dung(nguoi_dung_id: UUID, db: Session = Depends(get_db)):
    if not crud.xoa_nguoi_dung(db, nguoi_dung_id):
        raise HTTPException(status_code=404, detail="Không tìm thấy người dùng")
    return {"message": "Đã xóa người dùng"}

# =====================
# BỘ FLASHCARD (CRUD)
# =====================
@app.post("/bo-flashcard/{nguoi_dung_id}", response_model=schemas.BoFlashcardOut)
def tao_bo_flashcard(nguoi_dung_id: UUID, data: schemas.TaoBoFlashcard, db: Session = Depends(get_db)):
    return crud.tao_bo_flashcard(db, nguoi_dung_id, data.ten, data.mo_ta)

@app.get("/bo-flashcard", response_model=list[schemas.BoFlashcardOut])
def lay_tat_ca_bo_flashcard(db: Session = Depends(get_db)):
    return crud.lay_tat_ca_bo_flashcard(db)

@app.get("/bo-flashcard/{bo_id}", response_model=schemas.BoFlashcardOut)
def lay_bo_flashcard(bo_id: UUID, db: Session = Depends(get_db)):
    bo = crud.lay_bo_flashcard_theo_id(db, bo_id)
    if not bo:
        raise HTTPException(status_code=404, detail="Không tìm thấy bộ flashcard")
    return bo

@app.get("/bo-flashcard/nguoi-dung/{nguoi_dung_id}")
def lay_danh_sach_bo_flashcard(nguoi_dung_id: UUID, db: Session = Depends(get_db)):
    return crud.lay_danh_sach_bo_flashcard(db, nguoi_dung_id)

@app.put("/bo-flashcard/{bo_id}", response_model=schemas.BoFlashcardOut)
def cap_nhat_bo_flashcard(bo_id: UUID, data: schemas.CapNhatBoFlashcard, db: Session = Depends(get_db)):
    bo = crud.cap_nhat_bo_flashcard(db, bo_id, data.ten, data.mo_ta)
    if not bo:
        raise HTTPException(status_code=404, detail="Không tìm thấy bộ flashcard")
    return bo

@app.delete("/bo-flashcard/{bo_id}")
def xoa_bo_flashcard(bo_id: UUID, db: Session = Depends(get_db)):
    if not crud.xoa_bo_flashcard(db, bo_id):
        raise HTTPException(status_code=404, detail="Không tìm thấy bộ flashcard")
    return {"message": "Đã xóa bộ flashcard"}

# =====================
# FLASHCARD (CRUD)
# =====================
@app.post("/flashcard/{bo_id}", response_model=schemas.FlashcardOut)
def tao_flashcard(bo_id: UUID, data: schemas.TaoFlashcard, db: Session = Depends(get_db)):
    return crud.tao_flashcard(db, bo_id, data.mat_truoc, data.mat_sau, data.vi_du)

@app.get("/flashcard", response_model=list[schemas.FlashcardOut])
def lay_tat_ca_flashcard(db: Session = Depends(get_db)):
    return crud.lay_tat_ca_flashcard(db)

@app.get("/flashcard/{flashcard_id}", response_model=schemas.FlashcardOut)
def lay_flashcard(flashcard_id: UUID, db: Session = Depends(get_db)):
    fc = crud.lay_flashcard_theo_id(db, flashcard_id)
    if not fc:
        raise HTTPException(status_code=404, detail="Không tìm thấy flashcard")
    return fc

@app.get("/flashcard/bo/{bo_id}")
def lay_flashcard_theo_bo(bo_id: UUID, db: Session = Depends(get_db)):
    return crud.lay_flashcard_theo_bo(db, bo_id)

@app.put("/flashcard/{flashcard_id}", response_model=schemas.FlashcardOut)
def cap_nhat_flashcard(flashcard_id: UUID, data: schemas.CapNhatFlashcard, db: Session = Depends(get_db)):
    fc = crud.cap_nhat_flashcard(db, flashcard_id, data.mat_truoc, data.mat_sau, data.vi_du)
    if not fc:
        raise HTTPException(status_code=404, detail="Không tìm thấy flashcard")
    return fc

@app.delete("/flashcard/{flashcard_id}")
def xoa_flashcard(flashcard_id: UUID, db: Session = Depends(get_db)):
    if not crud.xoa_flashcard(db, flashcard_id):
        raise HTTPException(status_code=404, detail="Không tìm thấy flashcard")
    return {"message": "Đã xóa flashcard"}

# =====================
# HỌC & SPACED REPETITION
# =====================
@app.get("/hoc/{nguoi_dung_id}")
def lay_flashcard_can_on(nguoi_dung_id: UUID, db: Session = Depends(get_db)):
    flashcards = db.query(models.Flashcard).all()

    result = []
    for fc in flashcards:
        tien_do = db.query(models.TienDoHoc).filter(
            models.TienDoHoc.nguoi_dung_id == nguoi_dung_id,
            models.TienDoHoc.flashcard_id == fc.id
        ).first()
        if not tien_do:
            # Tạo tiến độ học mới
            tien_do = crud.tao_tien_do_hoc(db, nguoi_dung_id, fc.id, date.today())
        result.append(tien_do)
    return result

@app.post("/hoc/{tien_do_id}")
def hoc_flashcard(tien_do_id: UUID, data: dict = Body(...), db: Session = Depends(get_db)):
    tien_do = db.query(models.TienDoHoc).filter(models.TienDoHoc.id == tien_do_id).first()
    if not tien_do:
        raise HTTPException(status_code=404, detail="Không tìm thấy tiến độ học")

    muc_do = data.get("muc_do")
    if muc_do is None:
        raise HTTPException(status_code=400, detail="Thiếu muc_do")

    cap_nhat_spaced_repetition(tien_do, muc_do)
    db.commit()
    db.refresh(tien_do)
    return {"message": "Đã cập nhật tiến độ học", "so_lan_on": tien_do.so_lan_on, "ngay_on_tiep": tien_do.ngay_on_tiep}
# =====================
# ĐĂNG NHẬP
# =====================
@app.post("/dang-nhap", response_model=schemas.NguoiDungOut)
def dang_nhap(data: schemas.DangNhap, db: Session = Depends(get_db)):
    nguoi_dung = crud.xac_thuc_nguoi_dung(db, data.email, data.mat_khau)
    if not nguoi_dung:
        raise HTTPException(status_code=401, detail="Email hoặc mật khẩu không đúng")
    return nguoi_dung

@app.put("/nguoi-dung/{nguoi_dung_id}", response_model=schemas.NguoiDungOut)
def doi_mat_khau(nguoi_dung_id: UUID, data: dict = Body(...), db: Session = Depends(get_db)):
    mat_khau_moi = data.get("mat_khau")
    if not mat_khau_moi:
        raise HTTPException(status_code=400, detail="Thiếu mat_khau")
    
    nd = crud.cap_nhat_mat_khau(db, nguoi_dung_id, mat_khau_moi)
    if not nd:
        raise HTTPException(status_code=404, detail="Không tìm thấy người dùng")
    return nd