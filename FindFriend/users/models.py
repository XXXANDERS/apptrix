from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

# username_validator = UnicodeUsernameValidator()
from users.manager import CustomUserManager


class CustomUser(AbstractUser):
    SEX_CHOICES = (
        (None, 'Не выбран'),
        (1, 'Мужской'),
        (2, 'Женский'),
    )
    username = None
    email = models.EmailField(_('email address'), blank=False, unique=True)
    avatar = models.ImageField(upload_to="avatars/%Y/%m/%d/", blank=True)
    sex = models.BooleanField(choices=SEX_CHOICES, blank=True, null=True, default=None)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ()
    objects = CustomUserManager()
