import base64

from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from recipes.models import Ingredient, RecipeIngredient
from rest_framework import serializers, status
from rest_framework.response import Response


class Base64ImageField(serializers.ImageField):
    """Вспомогательный класс для работы с изображениями."""
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


def create_ingredients(ingredients, recipe):
    """Функция добавления ингредиентов при создании/редактировании рецепта."""
    ingredient_list = []
    for ingredient in ingredients:
        current_ingredient = get_object_or_404(
            Ingredient, id=ingredient.get('id')
        )
        amount = ingredient.get('amount')
        ingredient_list.append(
            RecipeIngredient(
                recipe=recipe, ingredient=current_ingredient, amount=amount
            )
        )
    RecipeIngredient.objects.bulk_create(ingredient_list)


def create_model_instance(request, recipe_id, serializer_name):
    """Функция для добавления рецепта в избранное или список покупок."""
    serializer = serializer_name(
        data={'user': request.user.id, 'recipe': recipe_id},
        context={'request': request}
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


def delete_model_instance(request, model, instance):
    """Функция для удаления рецепта из избранного или из списка покупок."""
    recipe = get_object_or_404(model, user=request.user, recipe=instance)
    recipe.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
