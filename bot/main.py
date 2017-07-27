import asyncio
import logging
import sys
from operator import attrgetter
from random import choice

from config import config
from exceptions import NoAvailablePostsLeft
from manager import Manager


class Bot:

    def __init__(self):
        self.log = logging.getLogger(__name__ + "." + str(self.__class__))
        self.manager = Manager()

    def get_post_for_likes(self, user):
        user_ids_with_unliked_posts = {
            post.author for post in self.manager.posts
            if post.likes_count == 0 and post.author != user.id
        }

        try:
            return choice([
                post for post in self.manager.posts
                if (
                    post.author in user_ids_with_unliked_posts and
                    post.id not in user.liked_posts
                )
            ])
        except IndexError:
            return

    async def perform_likes_by_user(self, user):
        while len(user.liked_posts) < config.max_likes_per_user:
            post = self.get_post_for_likes(user)
            if not post:
                self.log.info('No available posts for this user')

                raise NoAvailablePostsLeft

            await self.manager.like_post(post, user)

    async def perform_likes(self):
        self.log.info('Start to perform likes')

        for user in sorted(self.manager.users,
                           key=attrgetter('posts_count'), reverse=True):
            self.log.info('User #{} start to perform likes'.format(user.id))

            try:
                await self.perform_likes_by_user(user)
            except NoAvailablePostsLeft:
                continue

    async def go(self):
        self.log.info('Bot launched')

        await self.manager.create_users_and_posts(
            users_count=config.number_of_users,
            max_posts_per_user=config.max_posts_per_user
        )

        await self.perform_likes()


def main():
    log = logging.getLogger(__name__)

    logging.basicConfig(
        format='%(levelname)-8s [%(asctime)s] %(message)s', level=logging.INFO
    )

    bot = Bot()
    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(bot.go())
        log.info('Posts: {}'.format(bot.manager.posts))
    except Exception:
        return 1
    else:
        return 0

if __name__ == '__main__':
    sys.exit(main())
