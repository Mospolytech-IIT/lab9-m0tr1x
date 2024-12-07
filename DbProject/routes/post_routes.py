
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_db
from schemas import PostCreate, Post
from step2_operations import add_posts, get_all_posts_with_users, update_post_content, delete_post

router = APIRouter(tags=["posts"])


@router.post("/posts/", response_model=Post)
async def create_post(post: PostCreate, session: AsyncSession = Depends(get_db)):
    # Используем функцию для добавления постов
    await add_posts([post.dict()], session)
    return post


@router.get("/posts/", response_model=list[Post])
async def get_posts(session: AsyncSession = Depends(get_db)):
    """THis function returns all posts"""
    posts = await get_all_posts_with_users(session)
    return posts

@router.put("/posts/{post_id}", response_model=Post)
async def update_post(post_id: int, new_content: str, session: AsyncSession = Depends(get_db)):
    """THis function updates a post"""
    await update_post_content(post_id, new_content, session)
    post = await get_all_posts_with_users(session)
    return post


@router.delete("/posts/{post_id}")
async def delete_post(post_id: int, session: AsyncSession = Depends(get_db)):
    """This function deletes a post"""
    await delete_post(post_id, session)
    return {"message": "Post deleted"}
