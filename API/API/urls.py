
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from django.conf.urls.static import static
from ProductApi import views
import os
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )
from knox import views as knox_views
from . import settings


router = DefaultRouter()
router.register('Product', views.ProductApi)
router.register('Categories', views.CategoriesApi)
router.register('Shop', views.ShopApi)
router.register('Color', views.ColorApi)
router.register('test', views.TestImage)
router.register('profile', views.Profile)
router.register('comment', views.CommentView)
router.register('rating', views.RatingView)
router.register('ouradds', views.OurAddsView)
router.register('like', views.LikeView)
router.register('news',views.NewsViews)
router.register('jobs',views.JobsViews)
# router.register('freecredit',views.FreeCredit)
# router.register('followers', views.FollowerView)

# router.register('Product/category/<id:int>',views.ProductCategoryApi)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.Home),
    path('api-auth/', include('rest_framework.urls')),
    path('api/docs/kaznikaz/version1/', include(router.urls)),
    path('api/chat/',include('Chat.urls')),
    path('api/Product/shop/<int:id>', views.ShopProduct.as_view()),
    path('api/docs/kaznikaz/version1/Product/category/<int:id>', views.ProductCategoryApi.as_view()),
    path('api/docs/kaznikaz/version1/userProducts/<int:id>',views.UserProducts.as_view()),
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/docs/kaznikaz/version1/login', views.Login.as_view()),
    path('api/docs/kaznikaz/version1/user', views.AuthUser.as_view()),
    path('api/docs//kaznikaz/version1/userpr',views.UserAPI.as_view()),
    path('api/docs/kaznikaz/version1/signup', views.UserRegister.as_view()),
    path('api/docs/kaznikaz/version1/logout', knox_views.LogoutView.as_view()),
    path('api/docs/kaznikaz/version1/logoutall', knox_views.LogoutAllView.as_view()),
    path('api/docs/kaznikaz/version1/userprofile/<int:id>', views.Getprofile.as_view()),
    path('api/docs/kaznikaz/version1/shoplogin', views.ShopLogin.as_view()),
    path('api/docs/kaznikaz/version1/shop/<int:shopid>', views.SingleShop.as_view()),
   
    path('api/docs/kaznikaz/version1/shopcomment/<int:id>', views.ShopComment.as_view()),
    path('api/docs/kaznikaz/version1/shopLike/<int:id>', views.ShopLike.as_view()),
    path('api/docs/kaznikaz/version1/shoprate/<int:id>', views.ShopRating.as_view()),
    path('api/docs/kaznikaz/version1/userlike/<int:uid>/<int:sid>', views.UserLikeView.as_view()),
    path('api/docs/kaznikaz/version1/childCategory/<int:id>', views.ChildCategory.as_view()),
    path('api/docs/kaznikaz/version1/userfollow/<int:uid>/<int:sid>', views.UserFollowerView.as_view()),
    path('api/docs/kaznikaz/version1/shopfollowers/<int:sid>', views.shopFollowView.as_view()),
    path('api/docs/kaznikaz/version1/discount', views.Discount.as_view()),
    path('api/docs/kaznikaz/version1/notification', views.NotificationView.as_view()),
    path('api/docs/kaznikaz/version1/notification/<str:uid>/<str:notification_id>/read',
         views.NotificationView.as_view()),
    path('api/docs/kaznikaz/version1/app_notifications', views.AppNotification.as_view()),
    path('api/docs/kaznikaz/version1/other_notifications/<int:uid>', views.OtherNotification.as_view()),
    path('api/docs/kaznikaz/version1/myshops/<int:uid>', views.UserShops.as_view()),
    # path('callback', views.CallBack.as_view()),
    # path('authpay', views.AuthPayment),
    path('api/docs/kaznikaz/version1/pay', views.Pays),
     path('api/docs/kaznikaz/version1/callback', views.callBack),
    # path('api/social/google/', views.GoogleLogin.as_view(), name='google_login'),
    path('api/docs/kaznikaz/version1/auth/', include('allauth.urls')),
    path('api/docs/kaznikaz/version1/google', views.validate_google_token),
    path('api/docs/kaznikaz/version1/facebook', views.get_facebook_user_data),
    path('api/docs/kaznikaz/version1/sendemail', views.send_email),
    path('api/docs/kaznikaz/version1/getcode', views.getCode),
    path('api/docs/kaznikaz/version1/verify', views.VerifyCode),
    path('api/docs/kaznikaz/version1/updatepass', views.NewPassword),
    path('api/docs/kaznikaz/version1/shopcode', views.CreateShopCode),
    path('api/docs/kaznikaz/version1/shopverify', views.VerifyCode),
    path('api/docs/kaznikaz/version1/shoppass', views.ResetShopPassword.as_view()),
    path('api/docs/kaznikaz/version1/editShop/<int:shop_id>', views.EditShop.as_view()),
    # path('api/docs/kaznikaz/version1/verification',views.faceVerification),
    path('api/docs/kaznikaz/version1/paymentStatus',views.CheckStatus),
    path('api/docs/kaznikaz/version1/freeCredits/<int:id>',views.CreditView),
    path('api/docs/kaznikaz/version1/normalProducts',views.NormalProduct.as_view()),
    path('api/docs/kaznikaz/version1/vipproducts',views.VipProduct.as_view()),
    path('.well-known/assetlinks.json', views.serve_assetlinks_json, name='assetlinks-json'),
    path('apple-app-site-association',views.app_serve_assetlinks_json,name='apple-app-site-association'),
    # path('api/docs/kaznikaz/version1/testpush',views.TestPush),
    path('api/docs/kaznikaz/version1/testnot',views.testNot),
    path('api/docs/kaznikaz/version1/registerToken',views.RegisterToken)
    
    # path('api/docs/kaznikaz/version1/news',views.NewsViews.as_view()),
    


]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# urlpatterns = [

#     path('products/',include('ProductApi.urls'))
# ]
