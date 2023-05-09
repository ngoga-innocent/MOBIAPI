from rest_framework import serializers 
from .models import Product,Shop,Categories,ProductImages

class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model=Shop
        fields='__all__'
  
class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model=Categories
        fields='__all__'

class ProductImageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=ProductImages
        fields='__all__'
  
class ProductSerializer(serializers.ModelSerializer):
    # category_name=CategoriesSerializer(read_only=True,many=True)
    proimages= ProductImageSerializer(many=True, read_only = True)
    uploaded_images=serializers.ListField(
        child=serializers.FileField(max_length=100000000,allow_empty_file=False,use_url=False),
        write_only=True
    )
    # uploaded_images = serializers.ListField(
    #     child = serializers.FileField(max_length = 1000000, allow_empty_file = False, use_url = False)
    #     write_only = True
    # )
    
    
    class Meta:
        model=Product
        fields=['id','title','description','price','rating','brand','category','thumbnail','seller','shop','proimages','uploaded_images']
    def create(self, validated_data):
            uploaded_images = validated_data.pop('uploaded_images')
            new_product = Product.objects.create(**validated_data)
            for image in uploaded_images:
                ProductImages.objects.create(product = new_product, Productimage = image)
            return new_product