from rest_framework import serializers
from .models import MenuItem
from decimal import Decimal
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
      model = Category
      fields=['id', 'slug', 'title']
class MenuItemSerializer(serializers.ModelSerializer):
    price_after_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    category=CategorySerializer
    class Meta:
        model=MenuItem
        fields='__all__'
    
    def calculate_tax(self, product:MenuItem):
        return product.price* Decimal(1.1)

"""class MenuItemSerializer(serializers.Serializer):
  id=serializers.IntegerField()
  title = serializers.CharField(max_length=255)"""