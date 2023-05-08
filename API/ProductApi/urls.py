from django.urls import path,include
# from .views import ProductList,ProductCreate
from rest_framework.routers import DefaultRouter
from . import views 


router=DefaultRouter()
router.register('Product',views.ProductApi)
router.register('Categories',views.CategoriesApi)
router.register('Shop',views.ShopApi)

urlpatterns = [
    path('',include(router.urls)),
    
    
]