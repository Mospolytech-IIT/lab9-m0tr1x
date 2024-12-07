"""This is the main file for the project"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from db import create_tables, get_db

from routes.user_routes import user_router
from routes.post_routes import post_router
from step2_operations import get_all_users, get_all_posts_with_users, \
    get_posts_by_user, update_user_email, update_post_content, \
    delete_post, delete_user_and_posts

app = FastAPI()

""" 
Ignored following pylint warnings:
    - `unused-argument`: 'app' is an unused parameter in the lifespan function, but it's required by FastAPI.
    - `redefined-outer-name`: 'app' is defined in the outer scope of the function (the parameter), 
      but we are using it in the context of the FastAPI framework's lifecycle.
    - `no-value-for-parameter`: Pylint is unable to detect that 'session' is correctly passed in the async context manager,
      because of the dynamic nature of the code execution.
"""


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
        await update_post_content(1, "new", "I was here", session)  # step 2 update post content
        await delete_post(2, session)  # step 2 delete post
        await delete_user_and_posts(1, session)  # step 2 delete user and his posts
        yield


app = FastAPI(lifespan=lifespan)

app.include_router(user_router)
app.include_router(post_router)
