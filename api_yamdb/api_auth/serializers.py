from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import (
    PasswordField, TokenObtainPairSerializer
)

User = get_user_model()


class TokenSerializer(TokenObtainPairSerializer):
    def __init__(self, *args, **kwargs):
        super(serializers.Serializer, self).__init__(*args, **kwargs)
        self.fields[self.username_field] = serializers.CharField()
        self.fields['confirmation_code'] = PasswordField()

    def validate(self, attrs):
        attrs['password'] = attrs['confirmation_code']
        return super(TokenSerializer, self).validate(attrs)


class AuthSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name',
            'username', 'bio',
            'email', 'role'
        )
        read_only_fields = ('role',)
