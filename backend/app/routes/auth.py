from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from ..services import auth as auth_service
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/api/auth", tags=["auth"]) 

@router.post("/register", response_model=schemas.User)
def register(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.email == user_in.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    # Ensure role exists
    role = db.query(models.Role).filter(models.Role.id == user_in.role_id).first()
    if not role:
        raise HTTPException(status_code=400, detail="Invalid role_id")
    hashed = auth_service.get_password_hash(user_in.password)
    user = models.User(email=user_in.email, full_name=user_in.full_name, hashed_password=hashed, role_id=user_in.role_id)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    if not auth_service.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    role_name = user.role.name if user.role else None
    access_token = auth_service.create_access_token(subject=user.email, extra={"role": role_name})
    return {"access_token": access_token, "token_type": "bearer"}

from ..dependencies import oauth2_scheme

@router.post('/logout')
def logout(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = auth_service.decode_token(token)
    jti = payload.get('jti') if payload else None
    if not jti:
        raise HTTPException(status_code=400, detail='Invalid token')
    # Persist revoked token
    from .. import models as _models
    rt = _models.RevokedToken(jti=jti)
    db.add(rt)
    db.commit()
    return {'detail': 'token revoked'}
