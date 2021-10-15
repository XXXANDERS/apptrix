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
        (0, 'Мужской'),
        (1, 'Женский'),
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

    sex = models.BooleanField(choices=SEX_CHOICES, blank=False, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ()
    objects = CustomUserManager()


class UserMatch(models.Model):
    LIKE_CHOICE = (
        (0, 'not liking'),
        (1, 'liking')
    )
    from_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='from_users')
    for_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='for_users')
    like = models.BooleanField(choices=LIKE_CHOICE, blank=False, null=False)

    def __str__(self):
        return f'{self.from_user.id} - {self.like} - {self.for_user.id}'

    class Meta:
        unique_together = ['from_user', 'for_user']
