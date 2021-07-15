from django.db import models
from django.contrib.auth.models import AbstractUser, UnicodeUsernameValidator
from django.utils.translation import ugettext_lazy as _

from .managers import UserManager


class User(AbstractUser):
    roles = (
        ('user', 'user',),
        ('moderator', 'moderator',),
        ('admin', 'admin',),
    )
    email = models.EmailField(
        _('email address'),
        unique=True,
        help_text=_('Required. For example: name@fake.com')
    )
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[UnicodeUsernameValidator()],
        error_messages={
            'unique': _('A user with that username already exists.'),
        },
        blank=True,
        null=True
    )
    bio = models.CharField(max_length=150, blank=True)
    role = models.CharField(choices=roles, default=roles[0], max_length=30)
    password = models.CharField(_('confirmation_code'), max_length=25)

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

    def __str__(self):
        return self.email[:20]
