from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

BCRYPT_MAX_BYTES = 72


def _truncate(password: str) -> str:
    """
    Ensure password fits bcrypt 72-byte limit.
    """
    password_bytes = password.encode("utf-8")[:BCRYPT_MAX_BYTES]
    return password_bytes.decode("utf-8", errors="ignore")


def hash_password(password: str) -> str:
    safe_password = _truncate(password)
    return pwd_context.hash(safe_password)


def verify_password(password: str, hashed: str) -> bool:
    safe_password = _truncate(password)
    return pwd_context.verify(safe_password, hashed)
