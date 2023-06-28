from rest_framework import serializers

from recipes.models import (Favorite, Ingredient, IngredientRecipe, Recipe,
                            ShoppingCard, Subscribe, Tag, TagRecipe)
from users.models import User


class UsersSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователя."""
    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name'
        )


class TokenSerializer(serializers.Serializer):
    """Сериализатор для получение JWT-токена."""
    class Meta:
        model = User
        fields = ('password', 'email')
