"""This module contains the routes for the posts"""
from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_db
from schemas import PostCreate
from step2_operations import add_posts, get_all_posts_with_users, \
    get_post_by_id, update_post_content, delete_post

post_router = APIRouter(prefix="/posts", tags=["posts"])
templates = Jinja2Templates(directory="templates")


# Страница создания поста
@post_router.get("/create", response_class=HTMLResponse)
async def create_post_page(request: Request):
    """Creation page"""
    return templates.TemplateResponse("post_form.html", {"request": request})


@post_router.post("/create")
async def create_post_post(
        title: str = Form(...),
        content: str = Form(...),
        user_id: int = Form(...),
        session: AsyncSession = Depends(get_db)
):
    """Post creation"""
    post = PostCreate(title=title, content=content, user_id=user_id)
    await add_posts([post.dict()], session)
    return RedirectResponse(url="/posts/", status_code=303)


@post_router.get("/edit/{post_id}", response_class=HTMLResponse)
async def edit_post_page(request: Request, post_id: int, session: AsyncSession = Depends(get_db)):
    """Post edit page"""
    post = await get_post_by_id(post_id, session)
    if not post:
        return HTMLResponse(content="Post not found", status_code=404)
    return templates.TemplateResponse("post_edit.html", {"request": request, "post": post})


@post_router.post("/edit/{post_id}")
async def edit_post(
        post_id: int,
        title: str = Form(...),
        content: str = Form(...),
        session: AsyncSession = Depends(get_db)
):
    """Editing post"""
    post = await get_post_by_id(post_id, session)
    if not post:
        return HTMLResponse(content="Post not found", status_code=404)

    await update_post_content(post_id, title, content, session)

    return RedirectResponse(url="/posts/", status_code=303)


@post_router.get("/delete/{post_id}", response_class=HTMLResponse)
async def delete_post_page(post_id: int, session: AsyncSession = Depends(get_db)):
    """Post delete"""
    await delete_post(post_id, session)
    return RedirectResponse(url="/posts/", status_code=303)


@post_router.get("/", response_class=HTMLResponse)
async def list_posts(request: Request, session: AsyncSession = Depends(get_db)):
    """All posts"""
    posts = await get_all_posts_with_users(session)
    return templates.TemplateResponse("posts.html", {"request": request, "posts": posts})
