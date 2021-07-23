from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser, UnicodeUsernameValidator
from django.contrib.auth.base_user import get_random_string
from django.contrib.auth.hashers import check_password, make_password

from .managers import UserManager


class Role:
    ROLES = (
        ('user', 'Пользователь',),
        ('moderator', 'Модератор',),
        ('admin', 'Администратор',),
    )
    roles = [role[0] for role in ROLES]
    ADMIN_PERM = roles[2:]
    MODERATOR_PERM = roles[1:]
    USER_PERM = roles


class User(AbstractUser):
    roles = Role.ROLES
    email = models.EmailField(
        _('email адресс'),
        unique=True,
        help_text=_('Обязательное поле! Пример: name@fake.com')
    )
    username = models.CharField(
        _('никнейм'),
        max_length=150,
        unique=True,
        help_text=_('Обязательное поле! '
                    '150 символов или меньше. Буквы, цифры и @ /./+/-/_'),
        validators=(UnicodeUsernameValidator(),),
        error_messages={
            'unique': _('Пользователь с таким никнеймом уже существует.'),
        },
        blank=False,
        null=True
    )
    bio = models.CharField(_('О себе.'), max_length=150, blank=True)
    role = models.CharField(choices=roles, default=roles[0][0], max_length=30)
    confirmation_code = models.CharField(
        _('confirmation_code'),
        max_length=128,
        default=get_random_string(4, '0123456789')
    )
    _confirmation_code = None

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email[:20]

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def set_confirmation_code(
            self, raw_password=get_random_string(4, '0123456789')):
        self.confirmation_code = make_password(raw_password)
        self._confirmation_code = raw_password

    def check_confirmation_code(self, raw_password):
        def setter(raw):
            self.set_confirmation_code(raw)
            self._confirmation_code = None
            self.save(update_fields=('password',))
        return check_password(raw_password, self.confirmation_code, setter)

    def get_short_name(self):
        name = (getattr(self, 'first_name', None)
                or getattr(self, 'username', None)
                or str(self).split('@')[0])
        return name

    def get_full_name(self):
        full_name = (self.last_name or None, self.first_name or None)
        if None in full_name:
            full_name = (
                (self.last_name or self.first_name)
                or self.get_short_name(),)
        return ' '.join(full_name)

    def save(self, *args, **kwargs):
        (self.is_staff,
         self.is_superuser) = (
            self.is_moderator,
            self.is_admin)
        super(User, self).save(*args, **kwargs)

    @property
    def is_admin(self):
        return self.role in Role.ADMIN_PERM

    @property
    def is_moderator(self):
        return self.role in Role.MODERATOR_PERM
