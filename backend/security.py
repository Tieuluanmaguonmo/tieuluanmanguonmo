from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def hash_mat_khau(mat_khau: str) -> str:
    # Giới hạn tối đa 72 byte cho bcrypt
    mat_khau_truncated = mat_khau.encode('utf-8')[:72].decode('utf-8', errors='ignore')
    return pwd_context.hash(mat_khau_truncated)

def verify_mat_khau(mat_khau: str, mat_khau_hash: str) -> bool:
    # Khi verify cũng nên truncate tương tự
    mat_khau_truncated = mat_khau.encode('utf-8')[:72].decode('utf-8', errors='ignore')
    return pwd_context.verify(mat_khau_truncated, mat_khau_hash)
