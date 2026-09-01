from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
import jwt
import uuid
from ..core.config import settings

# Use a pure-Python compatible scheme for development to avoid platform-specific bcrypt issues
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(subject: str, expires_delta: Optional[timedelta] = None, extra: dict = None) -> str:
    to_encode = {"sub": subject}
    if extra:
        to_encode.update(extra)
    # Add a unique identifier for token revocation tracking
    to_encode.update({"jti": uuid.uuid4().hex})
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt

def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        return payload
    except jwt.PyJWTError:
        return {}
