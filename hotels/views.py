from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions, response
from rest_framework.decorators import action

from .models import Hotel
from . import serializers
from .permissions import IsAuthor


# Create your views here.

class ProductViewSet(ModelViewSet):
    queryset = Hotel.objects.all()
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.ProductListSerializer
        return serializers.ProductSerializer

    def get_permissions(self):
        if self.action in ('update', 'partial_update', 'destroy'):
            return [permissions.IsAuthenticated(), IsAuthor() ]
        return [permissions.IsAuthenticatedOrReadOnly()]
