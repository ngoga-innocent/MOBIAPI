from django.contrib import admin
from .models import Categories,Product,Shop,Color,ProductImages,Test
# Register your models here.

admin.site.register(Categories)
admin.site.register(Product)
admin.site.register(Shop)
admin.site.register(Color)
admin.site.register( ProductImages)
admin.site.register(Test)