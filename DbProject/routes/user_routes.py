from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import HTMLResponse
from db import get_db
from schemas import UserCreate, User
from step2_operations import add_users, get_all_users, update_user_email, delete_user_and_posts, get_user_by_id, \
    update_user

templates = Jinja2Templates(directory="templates")

user_router = APIRouter(prefix="/users", tags=["users"])

@user_router.get("/", response_class=HTMLResponse)
async def list_users(request: Request, session: AsyncSession = Depends(get_db)):
    """Users Page"""
    users = await get_all_users(session)
    return templates.TemplateResponse("users.html", {"request": request, "users": users})

@user_router.get("/create", response_class=HTMLResponse)
async def create_user_page(request: Request):
    """User Create Page"""
    return templates.TemplateResponse("user_form.html", {"request": request})


@user_router.post("/create")
async def create_user_post(
        username: str = Form(...),
        email: str = Form(...),
        password: str = Form(...),
        session: AsyncSession = Depends(get_db)
):
    """User Creation"""

    user = UserCreate(username=username, email=email, password=password)

    # Добавляем пользователя в базу данных
    await add_users([user.dict()], session)

    return RedirectResponse(url="/users/", status_code=303)

@user_router.get("/edit/{user_id}", response_class=HTMLResponse)
async def edit_user_page(request: Request, user_id: int, session: AsyncSession = Depends(get_db)):
    """Edit User Page"""
    user = await get_user_by_id(user_id, session)
    return templates.TemplateResponse("user_edit.html", {"request": request, "user": user})


@user_router.post("/edit/{user_id}")
async def edit_user_post(
        user_id: int,
        username: str = Form(...),
        email: str = Form(...),
        password: str = Form(...),
        session: AsyncSession = Depends(get_db)
):
    """Editing User Page"""
    await update_user(user_id, username, email, password, session)
    return RedirectResponse(url="/users/", status_code=303)

@user_router.get("/delete/{user_id}")
async def delete_user_page(user_id: int, session: AsyncSession = Depends(get_db)):
    """Deleting user"""
    await delete_user_and_posts(user_id, session)
    return RedirectResponse(url="/users/", status_code=303)
