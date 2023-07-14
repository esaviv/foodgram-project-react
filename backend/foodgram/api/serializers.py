from api.utils import Base64ImageField, create_ingredients
from django.db import transaction
from djoser.serializers import UserCreateSerializer, UserSerializer
from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                            ShoppingCart, Tag)
from rest_framework import serializers
from users.models import Subscription, User


class UserSignUpSerializer(UserCreateSerializer):
    """Регистрации пользователей."""
    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'password')


class UserGetSerializer(UserSerializer):
    """Информацией о пользователях."""
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        request = self.context['request']
        return Subscription.objects.filter(
            user=request.user, author=obj
        ).exists()


class UserSubscribeRepresentSerializer(UserGetSerializer):
    """"Предоставление информации о подписках пользователя."""
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed', 'recipes', 'recipes_count')
        read_only_fields = ('email', 'username', 'first_name', 'last_name',
                            'is_subscribed', 'recipes', 'recipes_count')

    def get_recipes(self, obj):
        request = self.context['request']
        recipes_limit = request.query_params.get('recipes_limit')
        if recipes_limit:
            recipes = obj.recipes.all()[:int(recipes_limit)]
        recipes = obj.recipes.all()
        return RecipeSmallSerializer(recipes, many=True,
                                     context={'request': request}).data

    def get_recipes_count(self, obj):
        return obj.recipes.count()


class UserSubscribeSerializer(serializers.ModelSerializer):
    """Подписка/отписка от пользователей."""
    class Meta:
        model = Subscription
        fields = '__all__'


class TagSerialiser(serializers.ModelSerializer):
    """Работа с тегами."""
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    """Работа с ингредиентами."""
    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientGetSerializer(serializers.ModelSerializer):
    """Получение информации об ингредиентах при работе с рецептами."""
    id = serializers.IntegerField(source='ingredient.id', read_only=True)
    name = serializers.CharField(source='ingredient.name', read_only=True)
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit',
        read_only=True
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class IngredientPostSerializer(serializers.ModelSerializer):
    """Добавление ингредиентов при работе с рецептами."""
    id = serializers.IntegerField()
    amount = serializers.IntegerField()

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount')


class RecipeGetSerializer(serializers.ModelSerializer):
    """Получение информации о рецепте."""
    tags = TagSerialiser(many=True, read_only=True)
    author = UserGetSerializer(read_only=True)
    ingredients = IngredientGetSerializer(many=True, read_only=True,
                                          source='recipeingredients')
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField(required=False)

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'is_favorited', 'is_in_shopping_cart', 'name',
                  'image', 'text', 'cooking_time')

    def get_is_favorited(self, obj):
        request = self.context['request']
        return Favorite.objects.filter(
            user=request.user, recipe=obj
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context['request']
        return ShoppingCart.objects.filter(
            user=request.user, recipe=obj
        ).exists()


class RecipeSmallSerializer(serializers.ModelSerializer):
    """Краткая информация о рецепте."""
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class RecipeCreateSerializer(serializers.ModelSerializer):
    """Добаление/обновление рецепта."""
    ingredients = IngredientPostSerializer(
        many=True, source='recipeingredients'
    )
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('ingredients', 'tags', 'image',
                  'name', 'text', 'cooking_time')

    def validate(self, data):
        ingredients_list = []
        for ingredient in data.get('recipeingredients'):
            if ingredient.get('amount') <= 0:
                raise serializers.ValidationError(
                    'Количество не может быть меньше 1'
                )
            ingredients_list.append(ingredient.get('id'))
        if len(set(ingredients_list)) != len(ingredients_list):
            raise serializers.ValidationError(
                'Вы пытаетесь добавить в рецепт два одинаковых ингредиента'
            )
        return data

    @transaction.atomic
    def create(self, validated_data):
        request = self.context['request']
        ingredients = validated_data.pop('recipeingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(author=request.user, **validated_data)
        recipe.tags.set(tags)
        create_ingredients(ingredients, recipe)
        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        ingredients = validated_data.pop('recipeingredients')
        tags = validated_data.pop('tags')
        instance.tags.clear()
        instance.tags.set(tags)
        RecipeIngredient.objects.filter(recipe=instance).delete()
        super().update(instance, validated_data)
        create_ingredients(ingredients, instance)
        instance.save()
        return instance

    def to_representation(self, instance):
        request = self.context['request']
        return RecipeGetSerializer(
            instance, context={'request': request}
        ).data


class FavoriteSerializer(serializers.ModelSerializer):
    """Работа с избранными рецептами."""
    class Meta:
        model = Favorite
        fields = '__all__'


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Работа со списком покупок."""
    class Meta:
        model = ShoppingCart
        fields = '__all__'
