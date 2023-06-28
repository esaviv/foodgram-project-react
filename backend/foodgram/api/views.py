from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from .permissions import SelfEditUserOnlyPermission
from recipes.models import (Favorite, Ingredient, IngredientRecipe, Recipe,
                            ShoppingCard, Subscribe, Tag, TagRecipe)
from users.models import User

from .serializers import TokenSerializer, UsersSerializer


class TokenViewSet(APIView):
    """Получение JWT-токена в обмен на username и confirmation code."""
    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User, email=request.data.get('email')
        )
        if str(user.password) == request.data.get(
            'password'
        ):
            refresh = RefreshToken.for_user(user)
            token = {'auth_token': str(refresh.access_token)}
            return Response(
                token, status=HTTP_200_OK
            )
        return Response(
            {'password': 'Неверный пароль.'},
            status=HTTP_400_BAD_REQUEST
        )


class UsersViewSet(ModelViewSet):
    """Получение и редактирование информации о пользователях(-е).
    """
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    lookup_field = 'username'
    filter_backends = (SearchFilter,)
    search_fields = ('id',)
    http_method_names = ('get', 'post')

    @action(
        methods=['get'], detail=False,
        url_path='me', permission_classes=(SelfEditUserOnlyPermission,)
    )
    def me_user(self, request):
        user = get_object_or_404(
            User, id=request.id
        )
        print(request)
        serializer = self.get_serializer(user)
        return Response(serializer.data)
