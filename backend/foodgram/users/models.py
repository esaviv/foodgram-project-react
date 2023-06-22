from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, EmailField


class User(AbstractUser):
    email = EmailField(
        max_length=254, blank=False, null=False
    )
    first_name = CharField(
        max_length=150, blank=False, null=False
    )
    last_name = CharField(
        max_length=150, blank=False, null=False
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
