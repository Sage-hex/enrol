from fastapi import APIRouter, HTTPException, status

from app.core.store import store
from app.models import User
from app.schemas import UserCreate, UserRead

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate) -> UserRead:
    for user in store.users.values():
        if user.email == payload.email:
            raise HTTPException(status_code=409, detail="email already exists")

    user = User(id=store.next_user_id(), **payload.model_dump())
    store.users[user.id] = user
    return UserRead(**user.model_dump())


@router.get("", response_model=list[UserRead])
def get_users() -> list[UserRead]:
    return [UserRead(**user.model_dump()) for user in store.users.values()]


@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: int) -> UserRead:
    user = store.users.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    return UserRead(**user.model_dump())
