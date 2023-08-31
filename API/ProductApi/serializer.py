from rest_framework import serializers, validators
from .models import Product, Shop,Jobs, Categories, OurAdds,News, ProductImages, Color, FreeCredit,Test, Notification, ProfileImages, UserProfile, Comment, Like, Rating, UserFollow, ShopFollowers, UserLike
import base64
# from django.contrib.auth.models import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model

# User=get_user_model()
User = get_user_model()


class ShopSerializer(serializers.ModelSerializer):
    profile = serializers.ImageField(use_url=True, max_length=None)
    cover = serializers.ImageField(use_url=True, max_length=None)

    class Meta:
        model = Shop
        fields = ['id', 'name', 'profile', 'telephone',
                  'location', 'owner', 'password', 'cover', 'email', 'idCard', 'image']

        extra_kwargs = {
            "name": {
                "allow_blank": False,
                "required": True,
                "validators": [
                    validators.UniqueValidator(
                        Shop.objects.all(), "This name Already registered"
                    )
                ]
            }
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        name = validated_data.pop('name')
        truename = name.capitalize()

        hashed_password = make_password(password)
        shop = Shop.objects.create(
            password=hashed_password, name=truename, **validated_data)
        return shop


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = '__all__'


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = '__all__'


class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImages
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    shop = serializers.PrimaryKeyRelatedField(
        queryset=Shop.objects.all(), allow_null=True)
    colors = ColorSerializer(many=True)
    proimages = ProductImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(
            max_length=100000000, allow_empty_file=False, use_url=True),
        write_only=True
    )
    colors = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Color.objects.all())

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'rating', 'brand', 'category',
                  'thumbnail', 'seller', 'shop', 'proimages', 'uploaded_images', 'colors', 'discount', 'name', 'phone', 'IdCard','place','created_at']

    def create(self, validated_data):
        uploaded_images = validated_data.pop('uploaded_images')
        colors_data = validated_data.pop('colors')
        new_product = Product.objects.create(**validated_data)
        for image in uploaded_images:
            ProductImages.objects.create(
                product=new_product, Productimage=image)

        new_product.colors.set(colors_data)
        return new_product

    # def get_colors(self,data):
    #      colors=Color.objects.all()
    #      return data


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = '__all__'


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email', 'password',
                  'first_name', 'last_name', 'phone_number','device_token']

        extra_kwargs = {
            "password": {"write_only": True},
            "email": {
                "allow_blank": False,
                "required": True,
                "validators": [
                    validators.UniqueValidator(
                        User.objects.all(), "A user with that Email already registered"
                    )
                ]
            }

        }

    def create(self, validated_data):
        username = validated_data.get('username')
        email = validated_data.get('email')
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        password = validated_data.get('password')
        phone_number = validated_data.get('phone_number')
        device_token=validated_data.get('device_token')

        user = User(username=username, email=email,
                    first_name=first_name, last_name=last_name, phone_number=phone_number,device_token=device_token)

        user.set_password(password)
        user.save()
        return user
        # else:
        #     raise serializers.ValidationError({
        #         'error':'passwords do  not match'
        #     })


class ProfileImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileImages
        fields = "__all__"


class UserProfileSerializer(serializers.ModelSerializer):

    profileimages = ProfileImagesSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(
            max_length=100000000, allow_empty_file=False, use_url=True),
        write_only=True
    )

    class Meta:
        model = UserProfile
        fields = ['user', 'about', 'profile', 'coverPhoto',
                  'uploaded_images', 'profileimages']

    def create(self, validated_data):
        uploaded_images = validated_data.pop('uploaded_images')

        new_profile = UserProfile.objects.create(**validated_data)
        for image in uploaded_images:
            ProfileImages.objects.create(profile=new_profile, images=image)
        return new_profile


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'


class FollowersSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFollow
        fields = '__all__'


class ShopFollowersSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopFollowers
        fields = '__all__'


class UserLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLike
        fields = '__all__'


class OurAddsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OurAdds
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
        read_only_fields = ['recipient']
class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'
class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model=Jobs
        fields='__all__'
# class CreditSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = FreeCredit
#         fields = [ 'user', 'credit']

#     def create(self, validated_data):
#         user = validated_data.get('user')
#         if id:
#             # Update an existing item
#             item = FreeCredit.objects.get(user=user)
#             for attr, value in validated_data.items():
#                 setattr(item, attr, value)
#             item.save()
#         else:
#             # Create a new item
#             item = FreeCredit.objects.create(**validated_data)
#         return item