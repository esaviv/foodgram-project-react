from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response


class AddRemoveMixin:
    def add(self, request, serializer_class, data):
        serializer = serializer_class(
            data=data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def remove(self, model, data):
        object = get_object_or_404(model, **data)
        object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
