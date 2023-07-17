from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response


def add_delete_recipe(request, recipe_id, model, serializer):
    """Функция добавления и удаления рецепта из избранного и списка покупок."""
    if request.method == 'POST':
        serializer = serializer(
            data={'user': request.user.id, 'recipe': recipe_id},
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    recipe = get_object_or_404(model, user=request.user, recipe=recipe_id)
    recipe.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
