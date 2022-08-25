from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.helper.utils import get_hashed_password
from app.dependencies import get_db
from app.schema.user import User
from app.crud import user_crud

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
    responses={404: {"description": "Not found"}},
)

def decode_token(db, token):
    # This doesn't provide any security at all
    # Check the next version
    user_name = token.split("-")[0]
    print("username is:", user_name)
    user_dict = user_crud.get_user_by_email(db=db, email=user_name)
    user = User(id=user_dict.id, name=user_dict.name, email=user_dict.email, is_active=user_dict.is_active)
    return user


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    user = decode_token(db,token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@router.post("/token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user_dict = user_crud.get_user_by_email(db=db, email=form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    hashed_password = get_hashed_password(form_data.password)
    if not hashed_password == user_dict.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    user = User(id=user_dict.id, name=user_dict.name, email=user_dict.email, is_active=user_dict.is_active)
    return {"access_token": user.email+"-token", "token_type": "bearer"}


@router.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user