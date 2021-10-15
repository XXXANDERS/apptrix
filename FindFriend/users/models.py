from PIL import Image
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

# username_validator = UnicodeUsernameValidator()
from imagekit.models import ImageSpecField, ProcessedImageField
from pilkit.processors import ResizeToFill

from users.manager import CustomUserManager


class Watermark(object):
    def process(self, image):
        # img = Image.open('123.png')
        watermark = Image.open('watermark.png').convert("RGBA")
        image.paste(watermark, (0, 0), watermark)
        # image.save(self)
        return image


class CustomUser(AbstractUser):
    SEX_CHOICES = (
        (None, 'Не выбран'),
        (1, 'Мужской'),
        (2, 'Женский'),
    )
    username = None
    email = models.EmailField(_('email address'), blank=False, unique=True)
    # avatar = models.ImageField(upload_to='avatars/%Y/%m/%d/', blank=True)
    avatar = ProcessedImageField(upload_to='avatars/%Y/%m/%d/',
                                 processors=[
                                     ResizeToFill(500, 500),
                                     Watermark(),
                                 ],
                                 format='PNG',
                                 blank=True
                                 # options={'quality': 60}
                                 )

    sex = models.BooleanField(choices=SEX_CHOICES, blank=True, null=True, default=None)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ()
    objects = CustomUserManager()
