from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from jose import JWTError,jwt
from sqlalchemy.exc import IntegrityError
from fastapi.security import OAuth2PasswordBearer
from ..database import get_db
from .. import models, schema, security
from .. dependencies import get_current_user
router = APIRouter(
    prefix="/users",
    tags=["Users"]
)
@router.get("/")
def get_users(db:Session=Depends(get_db),current_user:models.User =Depends(get_current_user)):
    users=db.query(models.User).all()
    return{
        "data":
        [   
            {
            "id":user.id,
            "name":user.name,
            "email":user.email

            }
            for user in users

        ]
    }
@router.post("/",response_model=schema.UserOut,status_code=status.HTTP_201_CREATED)
def create_user(user:schema.UserCreate,db:Session=Depends(get_db)):
    existing_user = db.query(models.User).filter(
        models.User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(409, "Email already registered")

    hashed_password = security.hash_password(user.password)

    new_user = models.User(
        name=user.name,
        email=user.email,
        password_Hash=hashed_password
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(409, "Email already registered")

    return new_user
@router.post("/login",response_model=schema.Token)
def login(user:schema.UserLogin,db:Session=Depends(get_db)):
    db_user=db.query(models.User).filter(
        models.User.email == user.email
    ).first()
    if not db_user:
        raise HTTPException(403,"Invalid credentials")
    if not security.verify_password(
        user.password,
        db_user.password_Hash
    ):
        raise HTTPException(403,"inavlid credentials")
    access_token=security.create_access_token(
        {"sub":str(db_user.id)}
    )
    return{"access_token":access_token,
           "token_type":"bearer"}
@router.get("/{id}", response_model=schema.UserOut)
def get_user(
    id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if id != current_user.id:
        raise HTTPException(403, "Not authorized")

    return current_user

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if id != current_user.id:
        raise HTTPException(403, "Not authorized")

    db.delete(current_user)
    db.commit()

    return Response(status_code=204)