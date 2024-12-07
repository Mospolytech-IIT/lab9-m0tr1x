
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_db
from schemas import UserCreate, User
from step2_operations import add_users, get_all_users, update_user_email, delete_user_and_posts

router = APIRouter(tags=["users"])


@router.post("/users/", response_model=User)
async def create_user(user: UserCreate, session: AsyncSession = Depends(get_db)):
    """This func is used for user creation"""
    await add_users([user.dict()], session)
    return user


@router.get("/users/", response_model=list[User])
async def get_users(session: AsyncSession = Depends(get_db)):
    """This func is used for getting all users"""
    users = await get_all_users(session)
    return users



@router.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, new_email: str, session: AsyncSession = Depends(get_db)):
    """This func is used for updating user"""
    await update_user_email(user_id, new_email, session)
    user = await get_all_users(session)
    return user



@router.delete("/users/{user_id}")
async def delete_user(user_id: int, session: AsyncSession = Depends(get_db)):
    """This func is used for deleting user and his posts"""
    await delete_user_and_posts(user_id, session)
    return {"message": "User and posts deleted"}
