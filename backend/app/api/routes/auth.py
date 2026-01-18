from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.db.models.user import User
from app.db.models.auth_provider import AuthProvider
from app.security.password import hash_password, verify_password
from app.security.jwt import create_access_token


router = APIRouter(prefix="/auth", tags=["auth"])


class SignupRequest(BaseModel):
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


@router.post("/signup")
def signup(data: SignupRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    username = data.email.split("@")[0]

    user = User(
        email=data.email,
        username=username,
        profile_pic=None,
    )
    db.add(user)
    db.flush()  

    auth = AuthProvider(
        user_id=user.id,
        provider="local",
        password_hash=hash_password(data.password),
    )
    db.add(auth)
    db.commit()

    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    auth = (
        db.query(AuthProvider)
        .filter(
            AuthProvider.user_id == user.id,
            AuthProvider.provider == "local",
        )
        .first()
    )

    if not auth or not verify_password(data.password, auth.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}
