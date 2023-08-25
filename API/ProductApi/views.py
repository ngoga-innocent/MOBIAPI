from django.http import JsonResponse,HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product, Categories, ShopVerificationCode,Payment, FreeCredit,VerificationCode, Shop, Color, Test, UserProfile, OurAdds, Comment, Notification, Rating, Like, UserFollow, UserLike, ShopFollowers
from django.contrib.auth.models import User
from .serializer import ProductSerializer, ShopFollowersSerializer, NotificationSerializer, OurAddsSerializer, CategoriesSerializer, FollowersSerializer, ShopSerializer, ColorSerializer, TestSerializer, UserRegistrationSerializer, UserProfileSerializer, CommentSerializer, RatingSerializer, LikeSerializer, UserLikeSerializer,UserLoginSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import viewsets,permissions,generics
from rest_framework import filters
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.models import AuthToken
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
import secrets
import os
from rest_framework.generics import RetrieveAPIView
import requests
import json
from rest_framework.renderers import JSONRenderer
from django.views.decorators.csrf import csrf_exempt
import uuid
import facebook
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from social_django.utils import psa
from requests.exceptions import HTTPError
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.mail import send_mail
import random
import string
from django.utils import timezone
import json
# import face_recognition
# from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
User = get_user_model()

# from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
# from rest_auth.registration.views import SocialLoginView

### google Login ##########


def generate_verification_code():
    code = ''.join(random.choices(string.digits, k=6))
    return code


@api_view(('POST',))
def validate_google_token(request):
    try:
        # Specify the Google OAuth 2.0 client ID for your application
        CLIENT_ID = os.environ.get("GOOGLE_ID")
        token = request.data.get('token')
        # Verify and decode the token
        id_info = id_token.verify_token(
            token, google_requests.Request(), CLIENT_ID)

        # Check if the token is valid and retrieve user information
        if id_info['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Invalid token issuer.')

        # Return the user information
        User = get_user_model()
        user, created = User.objects.get_or_create(email=id_info['email'])
        # user.first_name = id_info['given_name']
        # user.last_name = id_info['family_name']
        user.username = id_info['given_name'] or id_info['family_name']
        user.set_unusable_password()
        user.save()
        _, token = AuthToken.objects.create(user)
        if created:
            credits=20000
            print ('user created',user.id)
            try:
                creditsuser=User.objects.get(pk=user.id)
                credit,created=FreeCredit.objects.update_or_create(user=creditsuser,defaults={'credits':credits})
                if created:
                    message='User with credits created'
                else:
                    message='user Credits Update'

                return Response({'message':message,'user_info': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            },'token': token},status=201 )
            except User.DoesNotExist:
                return Response({'message':'User not exists'},status=200)
        
        else:
            print('user just logged in')
            return Response({
            'user_info': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            },
            'token': token
        })

    except ValueError as e:
        print(f'Token validation failed: {str(e)}')
        return Response({'error': str(e)}, status=400)

############# Facebook ##################
def Home(request):
    return render(request,'Product/home.html')

@api_view(('POST',))
def get_facebook_user_data(request):
    # Or request.GET.get('access_token') if using query string
    access_token = request.data.get('access_token')
    client_id = os.environ.get("FB_ID")
    # Make a request to the Facebook Graph API
    url = f'https://graph.facebook.com/me?access_token={access_token}&fields=id,name,email&client_id={client_id}'
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        data = response.json()
        # Extract the relevant user data
        user_id = data['id']
        user_name = data['name']
        user_email = data.get('email')

        User = get_user_model()
        user, created = User.objects.get_or_create(username=user_name)

        user.username = user_name
        user.email = user_email
        user.set_unusable_password()
        user.save()
        _, token = AuthToken.objects.create(user)
        if created:
            credits=20000
            print ('user created',user.id)
            try:
                creditsuser=User.objects.get(pk=user.id)
                credit,created=FreeCredit.objects.update_or_create(user=creditsuser,defaults={'credits':credits})
                if created:
                    message='User with credits created'
                else:
                    message='user Credits Update'

                return Response({'message':message,'user_info': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            },'token': token},status=201 )
            except User.DoesNotExist:
                return Response({'message':'User not exists'},status=200)
        
        else:
            print('user just logged in')
            return Response({
            'user_info': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            },
            'token': token
        })
        # Perform further processing or save the user data in your Django database
        # ...

    else:
        return JsonResponse({'error': 'Failed to retrieve user data from Facebook'}, status=400)

#Product functions
class ProductApi(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'shop__name',
                     'seller__username', 'category__name']

#adding Color
class ColorApi(viewsets.ModelViewSet):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer
    filter_backends = [filters.SearchFilter]

#Categories API
class CategoriesApi(viewsets.ModelViewSet):
    queryset = Categories.objects.filter(parent__isnull=True)
    serializer_class = CategoriesSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


# class GoogleLogin(SocialLoginView):
#     adapter_class = GoogleOAuth2Adapter

#product with discount
class Discount(APIView):
    def get(self, request):
        queryset = Product.objects.filter(discount__gt=0)
        serializer = ProductSerializer(
            queryset, many=True, context={'request': request})

        if (queryset.exists()):
            discounted_product = serializer.data

            return Response(serializer.data)

        else:
            return Response({
                'msg': 'No Discounted product'
            })

#adding Shop
class ShopApi(viewsets.ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    def post(self, request):
        user = request.user
        if user.is_authenticated:
            serializer = ShopSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            shop = serializer.save()
            subject = "Shop Created"
            message = "Shop Account created Success"
            email = request.data.get('email')
            recipient = [email]
            from_email = settings.EMAIL_HOST_USER
            try:
                send_mail(subject, message, from_email, recipient)
            except:
                return Response('Failed to create Shop', status=200)
            return Response({
                "shop_info": {
                    "shop_name": shop.name,
                    "shop_profile": shop.profile,
                    "shop_tel": shop.telephone,
                    "user": user,

                }
            }, status=200)
        else:
            return Response({'error': 'you are not authenticated'}, status=400)
    # def put(self,request):
    #     serializer=ShopSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     shop=serializer.save()
    #     subject = "Shop Created"
    #     message = "Shop Account created Success"
    #     email = request.data.get('email')
    #     recipient = [email]
    #     from_email = settings.EMAIL_HOST_USER
    #     try:
    #             send_mail(subject, message, from_email, recipient)
    #     except:
    #         return Response('Failed to create Shop', status=200)
    #     return Response({
    #             "shop_info": {
    #                 "shop_name": shop.name,
    #                 "shop_profile": shop.profile,
    #                 "shop_tel": shop.telephone,
                    

    #             }
    #         }, status=200)
class ProductCategoryApi(APIView):

    def get(self, request, id):
        products = Product.objects.filter(category=id)
        serializer = ProductSerializer(
            products, many=True, context={'request': request})
        return Response(serializer.data)

class UserProducts(APIView):
    def get(self,request,id):
        products=Product.objects.filter(seller=id)
        serializer=ProductSerializer(products,many=True,context={'request':request})
        return Response(serializer.data)
class ShopProduct(APIView):
    def get(self, request, id):
        products = Product.objects.filter(shop=id)
        serializer = ProductSerializer(
            products, many=True, context={'request': request})

        return Response(serializer.data)


class ShopComment(APIView):
    def get(self, request, id):
        comments = Comment.objects.filter(shopid=id)
        serializer = CommentSerializer(
            comments, many=True, context={'request', request})

        return Response((serializer.data))


class ShopLike(APIView):
    def get(self, request, id):
        likes = Like.objects.filter(shopid=id)
        if likes.exists():
            serializer = LikeSerializer(
                likes, many=True, context={'request', request})
            like_info = serializer.data[0]

            return Response({
                'like_info': {
                    'likes': like_info.get('like'),
                    'dislikes': like_info.get('dislike')
                }
            })
        else:
            return Response({'msg': 'Not found'})

    def put(self, request, id):
        queryset = Like.objects.filter(shopid=id)
        if queryset.exists():
            user_like = queryset.first()
            serializer = LikeSerializer(user_like, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'msg': 'updated'})
            else:
                return Response(serializer.errors, status=400)
        else:
            serializer = LikeSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'msg': 'created'})
            else:
                return Response(serializer.errors, status=400)


class ShopRating(APIView):
    def get(self, request, id):
        comments = Rating.objects.filter(shopid=id)
        serializer = RatingSerializer(
            comments, many=True, context={'request', request})

        return Response((serializer.data))


class TestImage(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer


class UserRegister(APIView):
    def post(self, request):

        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = generate_verification_code()
        subject = "Kaz ni Kaz  Account Created"
        message = f"Your account has been created with the username: {request.POST['username']},password:  {request.POST['password']},code: {code}"
        recipient_list = [request.data['email']]
        from_email = settings.EMAIL_HOST_USER
        try:
            sent = send_mail(subject, message, from_email, recipient_list)
            if sent > 0:
                user = serializer.save()
                _, token = AuthToken.objects.create(user)

                return Response({
                    'user_info': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'phone_number': user.phone_number,
                    },
                    'token': token
                })
            else:
                return Response("failed to send Email", status=500)

        except Exception as e:
            return Response(str(e), status=500)
@csrf_exempt
@api_view(['POST','GET'])
def CreditView(request,id):
    credits=request.data.get('credit')
    userReceived=request.data.get('user')
    if request.method =='POST':
        try:
            user=User.objects.get(pk=id)
            credit,created=FreeCredit.objects.update_or_create(user=user,defaults={'credits':credits})
            if created:
                message='User with credits created'
            else:
                message='user Credits Update'

            return Response({'message',message},status=201 )
        except User.DoesNotExist:
            return Response({'message':'User not exists'},status=200)
        
    else:
        try:
           user=User.objects.get(pk=id)
           credit=FreeCredit.objects.get(user=user)
           if credit:
               return Response({credit.credits},status=200)
        except:
            return Response({"user not exists"},status=401)
            
        # 

    # usercredit=FreeCredit.objects.get(user=user)
    # if(usercredit):
    #     usercredit.credits=credits
    #     usercredit.save()
    # else:
    #     credit=FreeCredit.objects.create(user=user,credits=credits)
    #     return Response({'user credits create'},status=200)
    
 



# class Login(APIView):
#     def post(self, request):

#         serializer = AuthTokenSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data.get('user')
#         _, token = AuthToken.objects.create(user)

#         return Response({
#             'user_info': {
#                 'id': user.id,
#                 'username': user.username,
#                 'email': user.email
#             },
#             'token': token
#         }, status=200)


class Login(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not any([username]):
            return Response({'error': 'Please provide either username, email, or phone number.'}, status=400)

        user = None
        if username:
            user = User.objects.filter(username=username).first()
        if not user and '@' in username:
            user = User.objects.filter(email=username).first()
        if not user and username.isdigit():
            user = User.objects.filter(phone_number=username).first()

        if not user or not user.check_password(password):
            return Response({'error': 'Invalid credentials.'}, status=400)

        _, token = AuthToken.objects.create(user)

        return Response({
            'user_info': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'phone_number': user.phone_number
            },
            'token': token
        })


@api_view(['POST'])
def getCode(request):
    username = request.POST.get('username')

    try:
        user = User.objects.get(email=username)
    except:
        return Response("User not found", status=500)

    code = generate_verification_code()
    subject = "Verification Code"
    message = f"Dear {username}, Your Verification Code is {code}"
    recipient_list = [user.email]
    from_email = settings.EMAIL_HOST_USER
    VerificationCode.objects.create(code=code, username=username)
    send_mail(subject, message, from_email, recipient_list)
    return Response("success", status=200)


@api_view(['POST'])
def VerifyCode(request):
    code = request.POST.get('code')
    email = request.POST.get('email')
    # print(code, email)
    try:
        datacode = VerificationCode.objects.get(code=code, username=email)
    except:
        return Response("no matching Code", status=404)

    time = timezone.now()
    saved = datacode.created
    difference = time-saved

    if (difference.total_seconds() > 10*60):

        return Response("expired", status=401)
    else:
        return Response("matching", status=200)


@api_view(['POST'])
def NewPassword(request):
    new_pssword = request.POST.get('password')
    email = request.POST.get('email')
    try:
        user = User.objects.get(email=email)
        user.set_password(new_pssword)
        user.save()
        return Response({"success"}, status=200)
    except:
        return Response({"message:Error in Updating Password"}, status=401)


class AuthUser(APIView):
    def get(self, request):
        user = request.user
        

        if user.is_authenticated:
            return Response({
                'user_info': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'firstname': user.first_name,
                    'secondName': user.last_name
                }
            })
        else:
            return Response({'error': 'you are not logged in'}, status=401)
class UserAPI(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = UserLoginSerializer

    def get_object(self):
        return self.request.user

class Profile(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class Getprofile(APIView):
    def get(self, request, id):
        profile = UserProfile.objects.filter(user=id)
        serializer = UserProfileSerializer(
            profile, many=True, context={'request': request})
        return Response({
            'user_profile': serializer.data
        })


class ShopLogin(APIView):
    def post(self, request):

        name = request.data.get('name')
        password = request.data.get('password')
        # password = make_password(unpassword)

        try:
            shop = Shop.objects.get(name=name)

        except shop.DoesNotExist:
            return Response("Invalid Name or Passwpord", status=status.HTTP_401_UNAUTHORIZED)

        if not check_password(password, shop.password):
            return Response("Invalid Email or Password", status=status.HTTP_401_UNAUTHORIZED)
        serializer = ShopSerializer(shop)
        shop_info = serializer.data
        # Generate a 32-byte random hexadecimal token
        token = secrets.token_hex(32)

        return Response({
            'shop': {
                'shop_id': shop_info.get('id'),
                'shop_name': shop_info.get('name'),
                'shop_profile': shop_info.get('profile'),
                'shop_location': shop_info.get('location'),
                'shop_tel': shop_info.get('telephone'),
                'token': token

            }
        }, status=status.HTTP_200_OK)


@api_view(['POST'])
def send_email(request):
    subject = "Passowrd checking"
    message = 'Am testing the email sending'
    from_email = 'mobishop@gmail.com'
    recipient_list = ['ngogainnocent1@gmail.com']
    send_mail(subject, message, from_email, recipient_list)
    return Response("email sent", status=200)


class ResetShopPassword(APIView):
    def post(self, request):
        name = request.data.get('name')
        password = request.data.get('password')
        try:
            shop = Shop.objects.get(name=name)
        except shop.DoesNotExist:
            return Response("Shop does not exists", status=status.HTTP_401_UNAUTHORIZED)
        shop.password = make_password(password)
        shop.save()

        return Response("success", status=200)


@api_view(['POST'])
def CreateShopCode(request):
    name = request.POST.get('name')
    try:
        shop = Shop.objects.get(name=name)
        if (shop):
            code = generate_verification_code()
            ShopVerificationCode.objects.create(name=name, code=code)

            subject = "Shop code"
            message = f"shop verification code is {code}"
            recipient = [shop.email]
            from_email = settings.EMAIL_HOST_USER
            try:
                send_mail(subject, message, from_email, recipient)
                return Response('sent')
            except:
                return Response("not sent")

    except:
        return Response('no shop', status=404)


@api_view(['POST'])
def VerifyCode(request):
    code = request.POST.get('code')
    name = request.POST.get('name')
    # print(code, email)
    try:
        datacode = ShopVerificationCode.objects.get(code=code, name=name)
        time = timezone.now()
        saved = datacode.created
        difference = time-saved

        if (difference.total_seconds() > 10*60):

            return Response(" code expired", status=401)
        else:
            return Response("matching", status=200)
    except:
        return Response("Invalid verification Code", status=404)


class EditShop(APIView):
    def put(self, request,shop_id):
        
        try:
            shop = Shop.objects.get(pk=shop_id)
            
            try: 
                shop.location = request.data.get('location', shop.location)
                shop.telephone = request.data.get('phone_number', shop.telephone)
                shop.profile = request.data.get('profile', shop.profile)
                shop.cover = request.data.get('cover', shop.cover)
                shop.name=request.data.get('name', shop.name)
                print(shop.cover)
                shop.save()
                
               
                print(shop)
                subject = 'Shop Update'
                message = 'Shop information updated'
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [shop.email]
                send_mail(subject, message, from_email, recipient_list)
                return Response("success", status=200)
            except:
                return Response("failed to send Email",status=404)
        except ObjectDoesNotExist:
            return Response("shop not found", status=401)
        

       


class SingleShop(APIView):
    def get(self, request, shopid):
        queryset = Shop.objects.filter(id=shopid)

        serializer = ShopSerializer(
            queryset, context={"request": request}, many=True)

        if queryset:

            shop_info = serializer.data[0]
            return Response({
                'shop': {
                    'shop_id': shop_info.get('id'),
                    'shop_name': shop_info.get('name'),
                    'shop_profile': shop_info.get('profile'),
                    'shop_location': shop_info.get('location'),
                    'shop_tel': shop_info.get('telephone'),
                    'shop_cover': shop_info.get('cover'),
                    'shop_email':shop_info.get('email')

                }
            }, status=status.HTTP_200_OK)
        return Response('not found')


class CommentView(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class RatingView(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer


class LikeView(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer


class UserFollowerView(APIView):
    def get(self, request, uid, sid):
        queryset = UserFollow.objects.filter(shopid=sid, userid=uid)
        serializer = FollowersSerializer(
            queryset, many=True, context={'request': request})

        if queryset.exists():
            followers = serializer.data
            return Response({
                'followers': followers
            })
        else:
            return Response({'msg': ' user not followed this Shop'})

    def put(self, request, uid, sid):
        queryset = UserFollow.objects.filter(userid=uid, shopid=sid)
        if queryset.exists():
            user_like = queryset.first()
            serializer = FollowersSerializer(user_like, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'msg': 'updated'})
            else:
                return Response(serializer.errors, status=400)
        else:
            serializer = FollowersSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'msg': 'created'})
            else:
                return Response(serializer.errors, status=400)


class UserLikeView(APIView):
    def get(self, request, uid, sid):
        queryset = UserLike.objects.filter(userid=uid, shopid=sid)
        serializer = UserLikeSerializer(
            queryset, many=True, context={'request': request})
        if queryset.exists():
            return Response({
                'liked': serializer.data
            })

        else:
            return Response({
                'message': 'not Liked or disliked'
            })

    def put(self, request, uid, sid):
        queryset = UserLike.objects.filter(userid=uid, shopid=sid)
        if queryset.exists():
            user_like = queryset.first()
            serializer = UserLikeSerializer(user_like, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'msg': 'updated'})
            else:
                return Response(serializer.errors, status=400)
        else:
            serializer = UserLikeSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'msg': 'created'})
            else:
                return Response(serializer.errors, status=400)


class shopFollowView(APIView):
    def get(self, request, sid):
        queryset = ShopFollowers.objects.filter(shopid=sid)
        serializer = ShopFollowersSerializer(
            queryset, many=True, context={'request': request})

        if queryset.exists():
            followers = serializer.data[0]
            return Response({
                'followers': followers['followers']
            })
        else:
            return Response({'followers': 0})

    def put(self, request, sid):
        queryset = ShopFollowers.objects.filter(shopid=sid)
        if queryset.exists():
            shopfollowers = queryset.first()
            serializer = ShopFollowersSerializer(
                shopfollowers, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'msg': 'followers updated'})
            else:
                return Response(serializer.errors, status=400)
        else:
            serializer = ShopFollowersSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'msg': 'followers created'})
            else:
                return Response(serializer.errors, status=400)


class ChildCategory(APIView):
    def get(self, request, id):
        queryset = Categories.objects.filter(parent=id)
        serializer = CategoriesSerializer(queryset)

        if queryset.exists():
            # Get the first instance from the queryset
            serializer = CategoriesSerializer(queryset, context={
                                              "request": request}, many=True)
            return Response({'categories': serializer.data})
        else:
            return Response({
                'msg': 'done'
            }, status=404)


class OurAddsView(viewsets.ModelViewSet):
    queryset = OurAdds.objects.all()
    serializer_class = OurAddsSerializer


class NotificationView(APIView):
    def post(self, request):
        users = User.objects.all()
        notifications = []
        print(request.data)
        for user in users:
            notification = Notification(
                recipient=user,
                type=request.data.get('type'),
                is_read=False,
                message=request.data.get('message')

            )
            notification.save()
            notifications.append(notification)
        serializer = NotificationSerializer(notification)
        return Response({'msg': 'notification Sent'})

    def get(self, request):
        notifications = Notification.objects.all()
        serializer = NotificationSerializer(
            notifications, many=True, context={'request', request})
        return Response(serializer.data)

    def put(self, request, notification_id, uid):
        try:
            notification = Notification.objects.get(
                id=notification_id, recipient=uid)
        except Notification.DoesNotExist:
            return Response({'error': 'Notification not found'}, status=404)

        notification.is_read = True

        notification.save()

        serializer = NotificationSerializer(notification)
        return Response(serializer.data)


class AppNotification(APIView):
    def get(self, request):
        app_notification = Notification.objects.filter(
            type='app notification', is_read=False)
        serializer = NotificationSerializer(app_notification, many=True)

        return Response(serializer.data)


class OtherNotification(APIView):
    def get(self, request):
        notifications = Notification.objects.filter(
            type='other notification', is_read=False)
        serializer = NotificationSerializer(notifications, many=True)

        return Response(serializer.data)


class UserShops(APIView):
    def get(self, request, uid):
        queryset = Shop.objects.filter(owner=uid)
        serializer = ShopSerializer(
            queryset, many=True, )

        if (queryset.exists()):
            return Response(serializer.data)
        else:
            return Response({'msg': 'you haven\'nt created any Shop'})


class CallBack(APIView):
    def post(self, request):
        if request.method == 'POST':
            status = request.POST.get('chargedCommission')

            print(request.body)

            return Response({'msg': 'status'})
        else:
            return Response({'msg': 'no data found'})
        # # Create your views here.


# def AuthPayment(request):
#     url = "https://payments.paypack.rw/api/auth/agents/authorize"

#     payload = json.dumps({
#         "client_id": "3282d7d6-151f-11ee-a49d-dead99b23929",
#         "client_secret": "c4dcc4f37d3c74d3b58d6e2b893eee3eda39a3ee5e6b4b0d3255bfef95601890afd80709"
#     })

#     headers = {
#         'Content-Type': 'application/json',
#         'Accept': 'application/json',
#         # Replace <access_token> with the actual token value
#         'Authorization': 'Bearer {access_token}'
#     }

#     response = requests.post(url, headers=headers, data=payload)

#     return JsonResponse({'response': response.json()})
##################### OLtramz payment ############################################################


@csrf_exempt
@api_view(('POST',))
def Pays(request):
    payer_telephone_number = request.data.get('payerTelephoneNumber')
    amount = request.data.get('amount')
    currency = request.data.get('currency')
    description = request.data.get('description')
    callback_url = request.data.get('callbackUrl')
    merchantTransactionId = uuid.uuid4()
    credentials = {
        # 'client_id': 'mobishop',
        # 'grant_type': 'client_credentials',
        # 'client_secret': '78fd0071-dc5a-40b0-9776-27b823aba954',
        'client_id': os.environ.get("OLTRANZ_ID"),
        'grant_type': 'client_credentials',
        'client_secret': os.environ.get("OLTRANZ_SECRET"),
    }

    # Send Authentication request
    auth_response = requests.post(
        'https://auth.oltranz.com/auth/realms/api/protocol/openid-connect/token', data=credentials)

    # Check if the request was successful
    if auth_response.status_code == requests.codes.ok:
        # Access the response data
        data = auth_response.json()
        token = data['access_token']
        headers = {
            "Authorization": "Bearer " + token,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        payments = {
            'merchantTransactionId': str(merchantTransactionId),
            'payerTelephoneNumber': payer_telephone_number,
            'amount': amount,
            'currency': 'RWF',
            'description': 'payment',
            'callbackUrl': 'https://0c84-102-22-173-142.ngrok-free.app/callback'
            # 'callbackUrl':os.environ.get("CALLBACK_URL")
        }
        

        # Send Payments
        send_payments_response = requests.post(
            'https://payments.api.oltranz.com/api/v2/payments/mobile/collections',
            data=json.dumps(payments),
            headers=headers
        )
        response=send_payments_response.json()
        print(response)
        transId=response.get('basePayTransactionId')
        status=response.get('status')
        desc=response.get('description')
        payment=Payment(transId=transId,telephone=payer_telephone_number,amount=amount,statusCode=401,status=status,trackId=merchantTransactionId,description=desc)
        payment.save()

        return Response(send_payments_response.json(), content_type='application/json')
    else:
        # Handle the error case
        return Response({'error': 'Authentication failed'}, status=auth_response.status_code, content_type='application/json')


#################################################### Paypack payment ###############################
# def Pays(request):
#     if request.method == 'GET':
#         amount = request.GET.get('amount')
#         number = request.GET.get('number')
#         url = "https://payments.paypack.rw/api/transactions/cashin?Idempotency-Key=OldbBsHAwAdcYalKLXuiMcqRrdEcDGRv"

#         payload = json.dumps({
#             "amounts": amount,
#             "number": '0788886530'
#         })
#         headers = {
#             'Content-Type': 'application/json',
#             'Accept': 'application/json',
#             'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IktESkZHbCIsImVtYWlsIjoiYmlsbGlvbmRvbGxhcjAwNUBnbWFpbC5jb20iLCJtZXJjaGFudCI6IkdDSEtKNyIsInZlcmlmaWVkIjpmYWxzZSwiYWdlbnQiOiIzMjgyZDdkNi0xNTFmLTExZWUtYTQ5ZC1kZWFkOTliMjM5MjkiLCJ0eXBlIjoxLCJwZXJtIjoiMzI4MjNiNzgtMTUxZi0xMWVlLWE0OWQtZGVhZDk5YjIzOTI5IiwiZXhwIjoxNjg3OTAwMDAwLCJpYXQiOjE2ODc4OTkxMDAsImlzcyI6InBheXBhY2sucnciLCJzdWIiOiJhY2Nlc3MifQ.7GaGOCYtqgyxHGbiF3C-FhSyCJ8ZA6MvTj2vshhTse8'
#         }

#         response = requests.request("POST", url, headers=headers, data=payload)

#         print(response.text)

#         return JsonResponse({'response': response.json()})


@csrf_exempt
@api_view(('POST',))
def callBack(request):
    
    
    if request.method == 'POST':
        try:
            body_data = request.data
            payer_telephone_number = request.data.get('payerTelephoneNumber')
            amount = request.data.get('collectedAmount')
            currency = request.data.get('currency')
            description = request.data.get('description')
            trackId=request.data.get('trackId')
            transId=request.data.get('basePayTransactionId')
            status=request.data.get('status')
            statusCode=request.data.get('statusCode')
            # print(body_data)
            payment=Payment.objects.get(transId=transId)
            if payment:
                # print("found")
                # payment, created = Payment.objects.update_or_create(transId=transId,telephone=payer_telephone_number,amount=amount,statusCode=statusCode,status=status,trackId=transId,description=description)
                payment.status=status
                payment.statusCode=statusCode
                payment.description=description
                payment.save()
                if statusCode !=200:
                    return Response({'message':'failed'},status=401)
                else:
                    return Response({'message':'success'},status=200)

            else:
                print('payment not found')
                return Response({'message':'not found'},status=404)
            # payment.save()
            
         
              # Read the request body only once
            # data = json.loads(body_data)
            
            # Process the data and perform necessary actions
            
            # response_data = {'message': 'Callback data processed successfully'}
            # return Response({'message':body_data})
        except json.JSONDecodeError:
            return Response({'error': 'Invalid JSON data'})
    else:
        return Response({'error': 'Invalid request method'})
@csrf_exempt
@api_view(('POST',))
def CheckStatus(request):
    trackid=request.data.get('trackId')

    transaction=Payment.objects.get(transId=trackid)
    if transaction:
        try:
            print(transaction.status)
            Status=transaction.status
            if(Status=='SUCCESS'):
                return Response({'status':Status},status=200)
            elif(Status=='PENDING'):
                return Response({'status':Status},status=201)
            elif(Status=='UNKNOWN'):
                return Response({'status':'PENDING'},status=400)
            else:
                return Response({'status':Status},status=401)
        except:
            return Response({"message":"Not found"},status=404)

# # def Product_list(request):
# #     products=Product.objects.all()
# #     serializer=ProductSerializer(products,many=True)
# #     return Response(serializer.data)

# class ProductList(APIView):
#     def get(self,request):
#         products=Product.objects.all()
#         serializer=ProductSerializer(products,many=True)
#         return Response(serializer.data)

# class ProductCreate(APIView):
#     def post(self,request):
#         serializer=ProductSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)

#         else:
#             return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
def serve_assetlinks_json(request):
    assetlinks_json_path = os.path.join(settings.BASE_DIR, '.well-known', 'assetlinks.json')
    with open(assetlinks_json_path, 'r') as file:
        return HttpResponse(file.read(), content_type='application/json')
# @csrf_exempt
# @api_view(('POST',))
# def faceVerification(request):
#     if request.method=='POST':
#         try:
#             id_image=request.FILES['Idcard']
#             selfie=request.FILES['image']

#             id_Image=face_recognition.load_image_file(id_image)
#             selfie_Image=face_recognition.load_image_file(selfie)

#     #ectract facial features 
#             document_face_encoding = face_recognition.face_encodings(id_Image)[0]
#             selfie_face_encoding = face_recognition.face_encodings(selfie_Image)[0]

#      # Compare the facial features
#             similarity = face_recognition.face_distance([document_face_encoding], selfie_face_encoding)[0]
#     # Define a verification threshold (e.g., 0.6)
#             verification_threshold = 0.6
#             if similarity < verification_threshold:
                
#                 return JsonResponse({'message': 'KYC verified'},status=200)
#             else:
#                 return JsonResponse({'message': 'Face verification failed'},status=405)
#         except MultiValueDictKeyError as e:
#             return JsonResponse({'error':'error field not found'})
#     else:
#         return JsonResponse({'error':'invalid request method '},status=405)