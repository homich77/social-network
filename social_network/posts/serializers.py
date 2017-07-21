from django.contrib.auth import get_user_model
from rest_framework import serializers

from posts.models import Post
from users.serializers import SimpleUserSerializer

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    author = SimpleUserSerializer(default=serializers.CurrentUserDefault(),
                                  read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'author', 'text', 'date_posted')
