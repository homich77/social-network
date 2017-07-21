from rest_framework.decorators import detail_route
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from posts.models import Post
from posts.permissions import IsStaffOrAuthor
from posts.serializers import PostSerializer, PostWithLikesSerializer


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostWithLikesSerializer
    permission_classes = (IsAuthenticated, IsStaffOrAuthor)

    def get_serializer_class(self):
        if self.action in ('list', 'like', 'unlike'):
            return PostSerializer

        return self.serializer_class

    @detail_route(methods=['POST'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        post = self.get_object()
        post.likes.add(request.user)
        serializer = self.get_serializer(post)
        return Response(serializer.data)

    @detail_route(methods=['POST'], permission_classes=[IsAuthenticated])
    def unlike(self, request, pk=None):
        post = self.get_object()
        post.likes.remove(request.user)
        serializer = self.get_serializer(post)
        return Response(serializer.data)
