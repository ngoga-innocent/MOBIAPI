"""
URL configuration for API project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from django.urls import path,include
from django.conf.urls.static import static
from ProductApi import views
from . import settings
router=DefaultRouter()
router.register('Product',views.ProductApi)
router.register('Categories',views.CategoriesApi)
router.register('Shop',views.ShopApi)
router.register('Color',views.ColorApi)
router.register('test',views.TestImage)
# router.register('Product/category/<id:int>',views.ProductCategoryApi)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include(router.urls)),
    path('Product/category/<int:id>',views.ProductCategoryApi.as_view())
    
    
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

# urlpatterns = [
   
#     path('products/',include('ProductApi.urls'))
# ]
