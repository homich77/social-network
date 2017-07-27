import asyncio
import logging
from random import randint

import factory

from client import Posts, Users
from factories import PostFactory, UserFactory
from models import Post, User

UsersClient = Users()
PostsClient = Posts()


class Manager:

    def __init__(self):
        self.log = logging.getLogger(__name__ + '.' + str(self.__class__))
        self.posts = []
        self.users = []

    async def create_user(self, data, **kwargs):
        user = User(**(
            await UsersClient.create_user(data=data, **kwargs)
        ))
        user.token = await UsersClient.login(
            data={'email': user.email, 'password': user.password}
        )

        self.users.append(user)
        return user

    async def create_post(self, data, **kwargs):
        post = Post(**(
            await PostsClient.create_post(data, **kwargs)
        ))

        self.posts.append(post)
        return post

    async def create_user_with_posts(self,  max_posts_per_user):
        user = await self.create_user(
            factory.build(dict, FACTORY_CLASS=UserFactory)
        )

        user.posts_count = randint(1, max_posts_per_user)

        await asyncio.gather(*[
            self.create_post(
                factory.build(dict, FACTORY_CLASS=PostFactory),
                headers=user.auth_headers
            ) for _ in range(user.posts_count)
        ])

    async def create_users_and_posts(self, users_count, max_posts_per_user):
        await asyncio.gather(*[
            self.create_user_with_posts(max_posts_per_user=max_posts_per_user)
            for _ in range(users_count)
        ])

        self.log.info('Users and posts created')

    async def like_post(self, post, user):
        await PostsClient.like_post(post.id, headers=user.auth_headers)

        post.likes_count += 1
        user.liked_posts.add(post.id)

        self.log.info(
            'User #{} liked post #{}(Author #{})'.format(
                user.id, post.id, post.author
            )
        )
