from rest_framework import serializers
from . import models

class BusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Business
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = '__all__'