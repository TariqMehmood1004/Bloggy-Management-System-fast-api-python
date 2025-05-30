from fastapi import APIRouter, Depends, Security, HTTPException
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from uuid import UUID
from ...schemas.user_schema import UserSchema
from ...models.user import User as UserModel
from ...models.token import Token as TokenModel
from ...utils.hash import hash_password
from ...utils.api_response_handler import APIResponse
from ...utils.catch_exception import catch_exception
from ...auth.jwt_handler import create_access_token
from ...config.config import SECRET_KEY, ALGORITHM
from ...database.database import get_db
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import desc



# Router
router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# --------------------

# Register
@router.post("/register")
@catch_exception
async def create_user(user: UserSchema, db: Session = Depends(get_db)):
    new_user = UserModel(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        username=user.username,
        is_admin=user.is_admin,
        password=hash_password(user.password)
    )

    # check if already exists
    if db.query(UserModel).filter(UserModel.username == user.username).first():
        return APIResponse.HTTP_409_CONFLICT(message="User already exists")

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return APIResponse.HTTP_201_CREATED(data=user.model_dump(), message="User created successfully")


# Login
@router.post("/login")
@catch_exception
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.username == form_data.username).first()
    if not user or not user.verify_password(form_data.password):
        return HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": str(user.id)})
    token_entry = TokenModel(user_id=user.id, token=access_token)
    db.add(token_entry)
    db.commit()

    return {"access_token": access_token, "token_type": "bearer"}


# Get user
@router.get("/users/me")
@catch_exception
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        current_user_id = UUID(payload.get("sub"))
    except (JWTError, ValueError):
        return APIResponse.HTTP_401_UNAUTHORIZED(message="Could not validate credentials")

    user = db.query(UserModel).filter(UserModel.id == current_user_id).first()
    if not user:
        return APIResponse.HTTP_404_NOT_FOUND(message="User not found")

    return APIResponse.HTTP_200_OK(data=user.to_dict(), message="User fetched successfully")


# Delete user based on current Token
@router.delete("/users/me/delete")
@catch_exception
async def delete_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        current_user_id = UUID(payload.get("sub"))
    except (JWTError, ValueError):
        return APIResponse.HTTP_401_UNAUTHORIZED(message="Could not validate credentials")

    # Delete related tokens first
    db.query(TokenModel).filter(TokenModel.user_id == current_user_id).delete()

    user = db.query(UserModel).filter(UserModel.id == current_user_id, UserModel.is_admin == False).first()
    if not user:
        return APIResponse.HTTP_404_NOT_FOUND(message="User not found")

    db.delete(user)
    db.commit()
    return APIResponse.HTTP_200_OK(message="User deleted successfully", data=user.to_dict())


# Delete all User except admin user
@router.get("/users/delete/all", response_model=UserSchema)
@catch_exception
async def delete_all_users_except_admin(token: str = Security(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = UUID(payload.get("sub"))
    except (JWTError, ValueError):
        return APIResponse.HTTP_401_UNAUTHORIZED(message="Could not validate credentials")

    # no need to delete the current account
    users = db.query(UserModel).filter(UserModel.is_admin == False).order_by(desc(UserModel.created_at)).all()
    if not users:
        return APIResponse.HTTP_404_NOT_FOUND(message="No users found")
    
    for user in users:
        db.delete(user)
    db.commit()
    
    return APIResponse.HTTP_200_OK(message="Users deleted successfully", data=[u.to_dict() for u in users])


# Delete User by user_id
@router.get("/users/delete/{user_id}")
@catch_exception
async def delete_any_user_by_authorized(user_id: UUID, token: str = Security(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        current_user_id = UUID(payload.get("sub"))
    except (JWTError, ValueError):
        return APIResponse.HTTP_401_UNAUTHORIZED(message="Could not validate credentials")

    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        return APIResponse.HTTP_404_NOT_FOUND(message="User not found")

    db.delete(user)
    db.commit()
    return APIResponse.HTTP_200_OK(message="User deleted successfully", data=user.to_dict())


# Users
@router.get("/users")
@catch_exception
async def get_users(token: str = Security(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = UUID(payload.get("sub"))
    except (JWTError, ValueError):
        return APIResponse.HTTP_401_UNAUTHORIZED(message="Could not validate credentials")

    users = db.query(UserModel).order_by(desc(UserModel.created_at)).all()
    return APIResponse.HTTP_200_OK(
        data=[u.to_dict() for u in users],
        message="Users fetched successfully"
    )


# ---------------------
