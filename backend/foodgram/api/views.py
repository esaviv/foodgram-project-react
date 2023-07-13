from django.db.models import Sum
from django.shortcuts import HttpResponse, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                            ShoppingCart, Tag)
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (
    AllowAny, IsAuthenticatedOrReadOnly, SAFE_METHODS
)
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import Subscription, User

from api.filters import IngredientFilter, RecipeFilter
from api.permissions import IsOwnerOrReadOnly
from api.serializers import (FavoriteSerializer, IngredientSerializer,
                             RecipeCreateSerializer, RecipeGetSerializer,
                             ShoppingCartSerializer, TagSerialiser,
                             UserSubscribeRepresentSerializer,
                             UserSubscribeSerializer)
from api.utils import create_model_instance, delete_model_instance


class UserSubscribeView(APIView):
    """Создание/удаление подписки на пользователя."""
    def post(self, request, user_id):
        author = get_object_or_404(User, id=user_id)
        serializer = UserSubscribeSerializer(
            data={'user': request.user.id, 'author': author.id},
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, user_id):
        author = get_object_or_404(User, id=user_id)
        if not Subscription.objects.filter(
            user=request.user, author=author
        ).exists():
            return Response(
                {'errors': 'Вы не подписаны на этого пользователя'},
                status=status.HTTP_400_BAD_REQUEST
            )
        Subscription.objects.get(user=request.user.id, author=user_id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserSubscriptionsViewSet(
    mixins.ListModelMixin, viewsets.GenericViewSet
):
    """Получение списка всех подписок на пользователей."""
    serializer_class = UserSubscribeRepresentSerializer

    def get_queryset(self):
        return User.objects.filter(following__user=self.request.user)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Получение информации о тегах."""
    queryset = Tag.objects.all()
    serializer_class = TagSerialiser
    permission_classes = (AllowAny, )
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Получение информации об ингредиентах."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny, )
    filter_backends = (DjangoFilterBackend, )
    filterset_class = IngredientFilter
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    """Работа с рецептами. Создание/изменение/удаление рецепта.
    Получение информации о рецептах.
    Добавление рецептов в избранное и список покупок.
    Отправка файла со списком рецептов.
    """
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.action in SAFE_METHODS:
            return RecipeGetSerializer
        return RecipeCreateSerializer

    @action(detail=True, methods=['post', 'delete'])
    def favorite(self, request, pk):
        """Удаление/добавление в избранное."""
        if request.method == 'POST':
            return create_model_instance(request, pk, FavoriteSerializer)
        return delete_model_instance(request, Favorite, pk)

    @action(detail=True, methods=['post', 'delete'])
    def shopping_cart(self, request, pk):
        """Удаление/добавление в список покупок."""
        if request.method == 'POST':
            return create_model_instance(request, pk, ShoppingCartSerializer)
        return delete_model_instance(request, ShoppingCart, pk)

    @action(detail=False, methods=['get'])
    def download_shopping_cart(self, request):
        """Отправка файла со списком покупок."""
        ingredients = RecipeIngredient.objects.filter(
            recipe__carts__user=request.user
        ).values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).annotate(ingredient_amount=Sum('amount'))
        shopping_list = ['Список покупок:\n']
        for ingredient in ingredients:
            name = ingredient['ingredient__name']
            unit = ingredient['ingredient__measurement_unit']
            amount = ingredient['ingredient_amount']
            shopping_list.append(f'\n{name} - {amount}, {unit}')
        response = HttpResponse(shopping_list, content_type='text/plain')
        response['Content-Disposition'] = (
            'attachment; filename="shopping_cart.txt"'
        )
        return response
