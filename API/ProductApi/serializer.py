from rest_framework import serializers 
from .models import Product,Shop,Categories,ProductImages,Color,Test
import base64

class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model=Shop
        fields='__all__'
  
class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model=Categories
        fields='__all__'
class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Color
        fields='__all__'
class ProductImageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=ProductImages
        fields='__all__'
  
class ProductSerializer(serializers.ModelSerializer):
    colors=ColorSerializer(many=True)
    # colors=serializers.SerializerMethodField()
    # category_name=CategoriesSerializer(read_only=True,many=True)
    proimages= ProductImageSerializer(many=True, read_only = True)
    uploaded_images=serializers.ListField(
        child=serializers.ImageField(max_length=100000000,allow_empty_file=False,use_url=True),
        write_only=True
    )
   
    colors=serializers.PrimaryKeyRelatedField(many=True,queryset=Color.objects.all())
    
    
    class Meta:
        model=Product
        fields=['id','title','description','price','rating','brand','category','thumbnail','seller','shop','proimages','uploaded_images','colors']
    def create(self, validated_data):
            uploaded_images = validated_data.pop('uploaded_images')
            colors_data=validated_data.pop('colors')
            new_product = Product.objects.create(**validated_data)
            for image in uploaded_images:
                ProductImages.objects.create(product = new_product, Productimage = image)

            new_product.colors.set(colors_data)
            return new_product
    # def get_colors(self,data):
    #      colors=Color.objects.all()
    #      return data
    
class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model=Test
        fields='__all__'