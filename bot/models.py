class BaseModel:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class User(BaseModel):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.liked_posts = set()
        self.posts = {}

    @property
    def auth_headers(self):
        return {'Authorization': 'JWT ' + self.token}

    def __str__(self):
        return '#{}. Email: {}'.format(self.id, self.email)

    __repr__ = __str__


class Post(BaseModel):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.likes_count = 0

    def __str__(self):
        return '#{}. Author: {}. Likes: {}'.format(
            self.id, self.author, self.likes_count
        )

    __repr__ = __str__
