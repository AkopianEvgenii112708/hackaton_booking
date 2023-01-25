from rest_framework import serializers
from category.models import Category
from .models import Hotel


class ProductListSerializer(serializers.ModelSerializer):
    owner_email = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Hotel
        fields = ('owner', 'owner_email', 'title', 'price', 'image', 'stock')


class ProductSerializer(serializers.ModelSerializer):
    owner_email = serializers.ReadOnlyField(source='owner.email')
    owner = serializers.ReadOnlyField(source='owner.id')
    class Meta:
        model = Hotel
        fields = '__all__'
