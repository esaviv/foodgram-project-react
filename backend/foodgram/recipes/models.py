from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=200)
    color = models.CharField(
        max_length=15,
        default='#FFFFFF'
    )
    slug = models.SlugField(
        unique=True,
        error_messages={'unique': 'Тег с этим слагом уже существует.'}
    )

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField()
    measurement_unit = models.CharField()


class Recipe(models.Model):
    ingredients = models.ForeignKey(
        Ingredient, on_delete=models.SET_NULL,
        related_name='recipes'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='recipes'
    )
    tags = models.ForeignKey(
        Tag, on_delete=models.SET_NULL,
        related_name='recipes'
    )
    image = models.ImageField(
        upload_to='recipes/'
    )
    name = models.CharField(max_length=200)
    text = models.TextField()
    cooking_time = models.IntegerField(min=1)

    def __str__(self):
        return self.text


class Subscribe(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="subscriber"
    )
    subscribing = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="subscribing"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "subscribing"], name="unique_subscribe"
            )
        ]


class Favorite(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "recipe"], name="unique_favorite"
            )
        ]
