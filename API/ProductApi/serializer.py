from rest_framework import serializers,validators
from .models import Product,Shop,Categories,ProductImages,Color,Test
import base64
from django.contrib.auth.models import User
# from django.contrib.auth import get_user_model

# User=get_user_model()

class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model=Shop
        fields='__all__'


        extra_kwargs={
              "name":{
                "allow_blank":False,
                "required":True,
                "validators":[
                    validators.UniqueValidator(
            Shop.objects.all(),"This name Already registered"
                    )
                ]
            }
        }
  
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

class UserRegistrationSerializer(serializers.ModelSerializer):
 
    class Meta:
        model=User
        fields=['username','email','password','first_name','last_name']

        extra_kwargs={
            "pasword":{"write_only":True},
            "email":{
                "allow_blank":False,
                "required":True,
                "validators":[
                    validators.UniqueValidator(
            User.objects.all(),"A user with that Email already registered"
                    )
                ]
            }

        }
    
    def create(self,validated_data):
        username=validated_data.get('username')
        email=validated_data.get('email')
        first_name=validated_data.get('first_name')
        last_name=validated_data.get('last_name')
        password=validated_data.get('password')
      

        user=User(username=username,email=email,first_name=first_name,last_name=last_name)
       
        user.set_password(password)
        user.save()
        return user
        # else:
        #     raise serializers.ValidationError({
        #         'error':'passwords do  not match'
        #     })
       
           