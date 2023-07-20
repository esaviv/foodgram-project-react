from django.contrib.auth.models import AbstractUser
from django.db import models

from django.conf import settings
from users.validators import validate_username


class User(AbstractUser):
    email = models.EmailField(
        'Электронная почта',
        max_length=settings.EMAIL_MAX_LENGTH, unique=True
    )
    username = models.CharField(
        'Имя пользователя',
        max_length=settings.USER_FIELDS_MAX_LENGTH, unique=True,
        validators=[validate_username, ]
    )
    first_name = models.CharField(
        'Имя', max_length=settings.USER_FIELDS_MAX_LENGTH
    )
    last_name = models.CharField(
        'Фамилия', max_length=settings.USER_FIELDS_MAX_LENGTH
    )
    password = models.CharField(
        'Пароль', max_length=settings.USER_FIELDS_MAX_LENGTH
    )

    class Meta:
        ordering = ('username', )
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Subscription(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='follower', verbose_name='Пользователь',
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='following', verbose_name='Автор',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'author'),
                name='unique_user_author'
            ),
            models.CheckConstraint(
                check=~models.Q(user=models.F('author')),
                name='check_user_not_author'
            )
        ]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'{self.user} подписался на {self.author}'
