from django.contrib import admin
from .models import Categories,DeviceTokens, Product,News, Shop, Color, FreeCredit,ProductImages, Notification, UserProfile, ProfileImages, ShopVerificationCode, VerificationCode, UserLike, UserFollow, CustomUser,ShopFollowers,Like,Payment
# Register your models here.
from django.contrib.auth import get_user_model
from .models import CustomUserManager
from django.contrib.auth.admin import UserAdmin

# class CustomUserAdmin(UserAdmin):
#     fieldsets=(
#         *UserAdmin.fieldsets,
#         ('Custom Fields',{'fields':('phone_number',)})
#     )
#     filter_horizontal = (*UserAdmin.filter_horizontal, )
#     list_filter = (*UserAdmin.list_filter, )

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
admin.site.register(FreeCredit)
admin.site.register(News)
admin.site.register(DeviceTokens)
admin.site.register(Notification)
# admin.site.register(CustomUser,CustomUserAdmin)

