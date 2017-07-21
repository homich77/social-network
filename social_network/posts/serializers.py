from django.contrib.auth import get_user_model
from rest_framework import serializers

from posts.models import Post
from users.serializers import SimpleUserSerializer

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    author = SimpleUserSerializer(default=serializers.CurrentUserDefault(),
                                  read_only=True)
    likes_count = serializers.IntegerField(source='likes.count',
                                           read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'author', 'text', 'date_posted', 'likes_count')


class PostWithLikesSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault()
    )
    likes = SimpleUserSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'author', 'text', 'date_posted', 'likes')
