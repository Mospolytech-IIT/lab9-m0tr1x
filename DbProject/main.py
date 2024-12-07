from db import create_tables, get_db
from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.templating import Jinja2Templates
from routes.user_routes import user_router
from routes.post_routes import post_router
from step2_operations import *


app = FastAPI()
templates = Jinja2Templates(directory="templates")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """This is the lifespan function."""
    async for session in get_db():
        await create_tables()  # step 1 create tables
        # await add_users(users_data, session)  # step 2 add users
        # await add_posts(posts_data, session)  # step 2 add posts
        usrs = await get_all_users(session)  # step 2 get all users
        psts = await get_all_posts_with_users(session)  # step 2 get all posts
        post_by_user = await get_posts_by_user(1, session)  # step 2 get posts by user
        print(f"Users got: {usrs}")
        print(f"Posts got: {psts}")
        print(f"Posts by user: {post_by_user}")
        await update_user_email(1, "grigory@gmail.com", session)  # step 2 update user email
        await update_post_content(1, "I was here", session)  # step 2 update post content
        await delete_post(2, session)  # step 2 delete post
        await delete_user_and_posts(1, session)  # step 2 delete user and his posts
        yield


app = FastAPI(lifespan=lifespan)


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


app.include_router(user_router)
app.include_router(post_router)
