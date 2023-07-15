from django.core.validators import MinValueValidator
from django.db import models

from foodgram.settings import (RECIPES_FIELDS_MAX_LENGTH,
                               SLUG_COLOR_MAX_LENGTH, TIME_AMOUNT)
from users.models import User


class Tag(models.Model):
    name = models.CharField(
        'Название', max_length=RECIPES_FIELDS_MAX_LENGTH, unique=True
    )
    color = models.CharField(
        'Цвет', max_length=SLUG_COLOR_MAX_LENGTH, unique=True
    )
    slug = models.SlugField(
        'Слаг', max_length=RECIPES_FIELDS_MAX_LENGTH, unique=True
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        'Название', max_length=RECIPES_FIELDS_MAX_LENGTH,
    )
    measurement_unit = models.CharField(
        'Единица измерения', max_length=RECIPES_FIELDS_MAX_LENGTH,
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_name_measurement_unit'
            )
        ]

    def __str__(self):
        return (f'{self.name}, {self.measurement_unit}')


class Recipe(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='recipes', verbose_name='Автор',
    )
    name = models.CharField(
        'Название', max_length=RECIPES_FIELDS_MAX_LENGTH,
    )
    image = models.ImageField(
        'Картинка', upload_to='recipes/',
    )
    text = models.TextField(
        'Описание',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient', verbose_name='Ингредиенты',
    )
    tags = models.ManyToManyField(
        Tag, verbose_name='Теги',
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления',
        validators=[
            MinValueValidator(
                TIME_AMOUNT,
                f'Время приготовления должно быть больше {TIME_AMOUNT} минуты.'
            )
        ]
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='recipeingredients', verbose_name='Рецепт'

    )
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE,
        related_name='recipeingredients', verbose_name='Ингредиент'
    )
    amount = models.PositiveSmallIntegerField(
        'Количество',
        validators=[
            MinValueValidator(
                TIME_AMOUNT,
                f'Количество ингредиентов должно быть больше {TIME_AMOUNT}.'
            )
        ]
    )

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецепте'

    def __str__(self):
        return (
            f'В рецепте {self.recipe} исп. '
            f'{self.ingredient} в кол-ве {self.amount}'
        )


class BaseUserRecipe(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, verbose_name='Рецепт',
    )

    class Meta:
        abstract = True
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='%(app_label)s_%(class)s_unique_relationships'
            )
        ]


class Favorite(BaseUserRecipe):
    class Meta:
        ordering = ['recipe']
        default_related_name = 'favorites'
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'

    def __str__(self):
        return f'{self.user} добавил {self.recipe} в избраннное'


class ShoppingCart(BaseUserRecipe):
    class Meta:
        ordering = ['user']
        default_related_name = 'carts'
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'

    def __str__(self):
        return (f'{self.user} добавил {self.recipe} в список покупок')
