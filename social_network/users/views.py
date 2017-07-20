from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from users.permissions import IsStaffOrTargetUser
from users.serializers import CreateUserSerializer, UserSerializer

User = get_user_model()


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsStaffOrTargetUser)

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateUserSerializer

        return self.serializer_class

    def get_permissions(self):
        if self.action == 'create':
            return AllowAny(),

        return super().get_permissions()
