
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from django.urls import path,include
from django.conf.urls.static import static
from ProductApi import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from knox import views as knox_views
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
    path('Product/category/<int:id>',views.ProductCategoryApi.as_view()),
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login',views.Login.as_view()),
    path('user',views.User.as_view()),
    path('signup',views.UserRegister.as_view()),
    path('logout',knox_views.LogoutView.as_view()),
    path('logoutall',knox_views.LogoutAllView.as_view()),
    
    
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

# urlpatterns = [
   
#     path('products/',include('ProductApi.urls'))
# ]
