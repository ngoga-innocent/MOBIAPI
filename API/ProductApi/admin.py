from django.contrib import admin
from .models import Categories,Product,Shop,Color,ProductImages,Test,UserProfile,ProfileImages
# Register your models here.

admin.site.register(Categories)
admin.site.register(Product)
admin.site.register(Shop)
admin.site.register(Color)
admin.site.register( ProductImages)
admin.site.register(UserProfile)
admin.site.register(ProfileImages)