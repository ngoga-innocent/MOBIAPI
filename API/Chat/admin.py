from django.contrib import admin

# Register your models here.
from .models import ChatAdmin,Code

admin.site.register(ChatAdmin)
admin.site.register(Code)