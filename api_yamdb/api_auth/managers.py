from django.contrib.auth.base_user import BaseUserManager, get_random_string
from django.conf import settings

from .permissions import (
    is_moderator_role as is_moder,
    is_admin_role as is_admin
)

ROLES = [role[0] for role in settings.USER_ROLES]


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('email должен быть указан')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, **extra_fields):
        extra_fields.setdefault('role', ROLES[0])
        extra_fields.setdefault('is_staff', is_moder(extra_fields.get('role')))
        extra_fields.setdefault('is_superuser', is_admin(extra_fields['role']))
        extra_fields.setdefault('password', self.make_random_password())
        return self._create_user(email, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', ROLES[2])

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

    def make_random_password(self, length=10, allowed_chars='1234567890'):
        return get_random_string(length, allowed_chars)
