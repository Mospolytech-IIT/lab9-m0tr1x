"""This module contains all the operations that can be performed on the step 2"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from models import User, Post


async def add_users(users_data: list, session: AsyncSession):
    """Adds a list of users to the database"""
    users = [User(username=user['username'], email=user['email'], password=user['password']) for user in users_data]
    session.add_all(users)
    await session.commit()
    print(f"{len(users)} users added.")


async def add_posts(posts_data: list, session: AsyncSession):
    """Adds a list of posts to the database"""
    posts = [Post(title=post['title'], content=post['content'], user_id=post['user_id']) for post in posts_data]
    session.add_all(posts)
    await session.commit()
    print(f"{len(posts)} posts added.")


async def get_all_users(session: AsyncSession):
    """This function gets all users from the database"""
    result = await session.execute(select(User))
    users = result.scalars().all()
    return users


async def get_user_by_id(user_id: int, session: AsyncSession):
    """This function finds a user by their id"""
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    return user

async def get_post_by_id(post_id: int, session: AsyncSession):
    """This function finds a user by their id"""
    result = await session.execute(select(Post).where(Post.id == post_id))
    post = result.scalars().first()
    return post


async def get_all_posts_with_users(session: AsyncSession):
    """This function retrieves all posts with their associated users and returns them."""
    result = await session.execute(
        select(Post).join(User).options(selectinload(Post.user))
    )
    posts = result.scalars().all()
    return posts


async def get_posts_by_user(user_id: int, session: AsyncSession):
    """This function retrieves all posts for a specific user"""
    result = await session.execute(select(Post).filter(Post.user_id == user_id))
    posts = result.scalars().all()
    return posts


async def update_user_email(user_id: int, new_email: str, session: AsyncSession):
    """This function updates the user's email address."""
    result = await session.execute(select(User).filter(User.id == user_id))
    user = result.scalar_one_or_none()
    if user:
        user.email = new_email
        await session.commit()
        print(f"Email updated for user {user.username} to {new_email}")
    else:
        print(f"User with id {user_id} not found.")

async def update_user(user_id: int, new_username: str, new_email: str, new_password: str, session: AsyncSession):
    """This function updates the user's email address and name"""
    result = await session.execute(select(User).filter(User.id == user_id))
    user = result.scalar_one_or_none()
    if user:
        user.username = new_username
        user.email = new_email
        user.password = new_password
        await session.commit()
        print(f"User {user.username} updated.")
    else:
        print(f"User with id {user_id} not found.")

async def update_post_content(post_id: int, new_content: str, session: AsyncSession):
    """This function updates the post's content"""
    result = await session.execute(select(Post).filter(Post.id == post_id))
    post = result.scalar_one_or_none()
    if post:
        post.content = new_content
        await session.commit()
        print(f"Content of post '{post.title}' updated.")
    else:
        print(f"Post with id {post_id} not found.")


async def delete_post(post_id: int, session: AsyncSession):
    """This function deletes a post from the database"""
    result = await session.execute(select(Post).filter(Post.id == post_id))
    post = result.scalar_one_or_none()
    if post:
        await session.delete(post)
        await session.commit()
        print(f"Post '{post.title}' deleted.")
    else:
        print(f"Post with id {post_id} not found.")


async def delete_user_and_posts(user_id: int, session: AsyncSession):
    """This function deletes all posts for a specific user"""
    result = await session.execute(select(User).filter(User.id == user_id))
    user = result.scalar_one_or_none()
    if user:
        result = await session.execute(select(Post).filter(Post.user_id == user_id))
        posts = result.scalars().all()
        for post in posts:
            await session.delete(post)
        await session.delete(user)
        await session.commit()
        print(f"User {user.username} and their posts deleted.")
    else:
        print(f"User with id {user_id} not found.")
