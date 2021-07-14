from django.db import models
from django.contrib.auth.models import AbstractUser, UnicodeUsernameValidator
from django.utils.translation import ugettext_lazy as _

from .managers import UserManager


class User(AbstractUser):
    roles = (
        ('U', 'user',),
        ('M', 'moderator',),
        ('A', 'admin',),
    )
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[UnicodeUsernameValidator()],
        error_messages={
            'unique': _("A user with that username already exists."),
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
            f'Ваш пароль: {raw_password}\n Не забудьте!')

    # def check_password(self, raw_password):
    #     return super(User, self).check_password(raw_password)

    def __str__(self):
        return self.email[:20]
