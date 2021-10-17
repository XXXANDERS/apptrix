from PIL import Image
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.mail import send_mail, BadHeaderError
from django.db import models
from django.utils.translation import gettext_lazy as _

from imagekit.models import ProcessedImageField
from pilkit.processors import ResizeToFill

from users.manager import CustomUserManager


class Watermark(object):
    def process(self, image):
        watermark = Image.open('watermark.png').convert("RGBA")
        image.paste(watermark, (0, 0), watermark)
        return image


def validate_latitude(value):
    if (value < -90) or (value > 90):
        raise ValidationError('Широта должна быть в пределах [-90, 90]', params={'value': value})


def validate_longitude(value):
    if (value < -180) or (value > 180):
        raise ValidationError('Долгота должна быть в пределах [-180, 180]', params={'value': value})


class CustomUser(AbstractUser):
    SEX_CHOICES = (
        (None, 'Не выбран'),
        (0, 'Мужской'),
        (1, 'Женский'),
    )
    username = None
    email = models.EmailField(_('email address'), blank=False, unique=True)
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
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True,
                                   validators=[validate_latitude])
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True,
                                    validators=[validate_longitude])

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

    # возможно лучше отправлять на уровне модели
    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     if self.like:
    #         match = UserMatch.objects.filter(from_user=self.for_user, for_user=self.from_user).first()
    #         if match and match.like:
    #             print('Взаимная симпатия !')
    #             subject = 'FindFriend response'
    #             try:
    #                 send_mail(
    #                     subject,
    #                     f'«Вы понравились {match.for_user.first_name} {match.for_user.last_name}! '
    #                     f'Почта участника: {match.for_user.email}»',
    #                     from_email=None, recipient_list=[f'{match.from_user.email}']
    #                 )
    #                 send_mail(
    #                     subject,
    #                     f'«Вы понравились {match.from_user.first_name} {match.from_user.last_name}! '
    #                     f'Почта участника: {match.from_user.email}»',
    #                     from_email=None, recipient_list=[f'{match.for_user.email}']
    #                 )
    #             except BadHeaderError as e:
    #                 print('Errors:', e)
