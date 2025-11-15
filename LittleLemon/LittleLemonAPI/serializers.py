from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from django.contrib.auth.models import User
from .models import MenuItem, Category, Rating
from decimal import Decimal


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
      model = Category
      fields=['id', 'slug', 'title']
class MenuItemSerializer(serializers.ModelSerializer):
    category_id=serializers.IntegerField(write_only=True)
    stock =serializers.IntegerField(source='inventory', read_only=True)
    price_after_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),   
        slug_field='slug'                  
    )
    class Meta:
        model=MenuItem
        fields='__all__'
        extra_kwargs = {
            'price': {'min_value':2},
            'inventory':{'min_value':0}
        }
    
    def calculate_tax(self, product:MenuItem):
        return product.price* Decimal(1.1)

class RatingSerializer(serializers.ModelSerializer):
    user=serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault()
    )
    class Meta:
        model=Rating
        fields=['user', 'menu_item_id', 'rating']
        validators= [UniqueTogetherValidator(queryset=Rating.objects.all(), fields=['user', 'menu_item_id', 'rating'])]
        extra_kwargs={
            'rating':{
                'max_value':5,
                'min_value':0
            }
        }
"""class MenuItemSerializer(serializers.Serializer):
  id=serializers.IntegerField()
  title = serializers.CharField(max_length=255)"""