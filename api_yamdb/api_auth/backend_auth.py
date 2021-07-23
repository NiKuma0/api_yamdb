from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class EmailOrUsernameModelBackend(ModelBackend):
    def authenticate(
            self, request, email=None,
            password=None, username=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(Q(email=email) | Q(email=username))
        except UserModel.DoesNotExist:
            return None
        if (user.check_password(password)
                or user.check_confirmation_code(password)):
            return user
        return None
