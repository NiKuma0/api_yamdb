from django.db import models
from django.contrib.auth.models import AbstractUser, UnicodeUsernameValidator
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from .managers import UserManager
from .permissions import is_admin_role, is_moderator_role

ROLES = settings.USER_ROLES


class User(AbstractUser):
    roles = ROLES
    email = models.EmailField(
        _('email адресс'),
        unique=True,
        help_text=_('Обязательное поле! Пример: name@fake.com')
    )
    username = models.CharField(
        _('никнейм'),
        max_length=150,
        unique=True,
        help_text=_('Обязательное поле! 150 символов или меньше. Буквы, цифры и @ /./+/-/_'),
        validators=[UnicodeUsernameValidator()],
        error_messages={
            'unique': _('Пользователь с таким никнеймом уже существует.'),
        },
        blank=True,
        null=True
    )
    bio = models.CharField(_('О себе.'), max_length=150, blank=True)
    role = models.CharField(choices=roles, default=roles[0][0], max_length=30)
    password = models.CharField(_('confirmation_code'), max_length=128)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def set_password(self, raw_password):
        super(User, self).set_password(raw_password)
        self.email_user(
            f'{self.get_short_name()}',
            f'Ваш пароль: {raw_password}\nНе забудьте!')

    def get_short_name(self):
        name = (getattr(self, 'first_name', None)
                or getattr(self, 'username', None)
                or str(self).split('@')[0])
        return name

    def get_full_name(self):
        full_name = (self.last_name or None, self.first_name or None)
        if None in full_name:
            full_name = ((self.last_name or self.first_name) or self.get_short_name(),)
        return ' '.join(full_name)

    def save(self, *args, **kwargs):
        if is_moderator_role(self.role):
            self.is_staff = True
        else:
            self.is_staff = False
        if is_admin_role(self.role):
            self.is_superuser = True
        else:
            self.is_superuser = False
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return self.email[:20]
