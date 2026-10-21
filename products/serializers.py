from rest_framework import serializers
from .models import *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class QuantityVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuantityVariant
        fields = '__all__'

class ColorVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColorVariant
        fields = '__all__'

class SizeVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = SizeVariant
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    quantity = QuantityVariantSerializer()
    color_type = ColorVariantSerializer()
    size_type = SizeVariantSerializer()

    class Meta:
        model = Product
        fields = '__all__'