from datetime import date, timedelta


def cap_nhat_spaced_repetition(tien_do, muc_do):
    # muc_do là "de" | "binh_thuong" | "kho"
    if muc_do == "de":
        tien_do.he_so_de += 0.15
        tien_do.khoang_cach_ngay = round(tien_do.khoang_cach_ngay * tien_do.he_so_de)
    elif muc_do == "binh_thuong":
        tien_do.khoang_cach_ngay = round(tien_do.khoang_cach_ngay * 1.5)
    elif muc_do == "kho":
        tien_do.khoang_cach_ngay = 1
        tien_do.he_so_de -= 0.2

    tien_do.so_lan_on += 1
    tien_do.lan_on_cuoi = date.today()
    tien_do.ngay_on_tiep = date.today() + timedelta(days=tien_do.khoang_cach_ngay)

    return tien_do
