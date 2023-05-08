from rest_framework import serializers 
from .models import Product,Shop,Categories

class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model=Shop
        fields='__all__'
  
class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model=Categories
        fields='__all__'
  
class ProductSerializer(serializers.ModelSerializer):
    category_name=CategoriesSerializer(read_only=True,many=True)
    
    class Meta:
        model=Product
        fields='__all__'