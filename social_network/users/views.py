from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from users.permissions import IsStaffOrTargetUser
from users.serializers import (
    CreateUserSerializer, DetailedUserSerializer, UserSerializer
)

User = get_user_model()


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = DetailedUserSerializer
    permission_classes = (IsAuthenticated, IsStaffOrTargetUser)
    serializer_action_classes = {
        'create': CreateUserSerializer,
        'list': UserSerializer
    }

    def get_serializer_class(self):
        serializer_for_action = self.serializer_action_classes.get(self.action)
        return serializer_for_action or self.serializer_class

    def get_permissions(self):
        if self.action == 'create':
            return AllowAny(),

        return super().get_permissions()
