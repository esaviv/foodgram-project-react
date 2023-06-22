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
        related_name='recipes', blank=True, null=True
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='recipes'
    )
    tags = models.ForeignKey(
        Tag, on_delete=models.SET_NULL,
        related_name='recipes', blank=True, null=True
    )
    image = models.ImageField(
        upload_to='recipes/', null=True, blank=True
    )
    name = models.CharField(max_length=200)
    text = models.TextField()
    cooking_time = models.IntegerField(min=1)

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )


class Follow(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="follower"
    )
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="following"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "following"], name="unique_follow"
            )
        ]
