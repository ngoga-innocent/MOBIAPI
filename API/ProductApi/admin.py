from django.contrib import admin
from .models import Categories, Product, Shop, Color, ProductImages, Test, UserProfile, ProfileImages, ShopVerificationCode, VerificationCode, UserLike, UserFollow, CustomUser,ShopFollowers,Like,Payment
# Register your models here.
from django.contrib.auth import get_user_model

admin.site.register(Categories)
admin.site.register(Product)
admin.site.register(Shop)
admin.site.register(Color)
admin.site.register(ProductImages)
admin.site.register(UserProfile)
admin.site.register(ProfileImages)
admin.site.register(UserLike)
admin.site.register(UserFollow)
admin.site.register(VerificationCode)
admin.site.register(ShopVerificationCode)
admin.site.register(get_user_model())
admin.site.register(ShopFollowers)
admin.site.register(Like)
admin.site.register(Payment)

