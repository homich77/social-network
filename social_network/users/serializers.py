from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.validators import EmailHunterValidate

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id', 'first_name', 'last_name', 'email', 'is_active', 'is_staff',
        )
        read_only_fields = ('email', 'is_active', 'is_staff')


class CreateUserSerializer(serializers.ModelSerializer):
    email = serializers.CharField(validators=[
        EmailHunterValidate(), UniqueValidator(
            queryset=User.objects.all(),
            message='User with this email already exists.'
        )
    ])

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'password')
        extra_kwargs = {
            'password': {
                'validators': [validate_password], 'write_only': True,
            },
        }

    def create(self, validated_data):
        return self.Meta.model.objects.create_user(**validated_data)


class SimpleUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name')
