from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    phone = models.CharField(unique=True, max_length=35, verbose_name='Номер телефона')

    email = models.EmailField(verbose_name='Почта', null=True, blank=True)
    avatar = models.ImageField(upload_to='users/', verbose_name='Аватар', null=True, blank=True)
    country = models.CharField(max_length=35, verbose_name='Страна', null=True, blank=True)
    nickname = models.CharField(max_length=100, verbose_name='Ник', null=True, blank=True)
    is_subscribed = models.BooleanField(default=False, verbose_name='Подписка')

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'Пользователь: {self.phone}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
