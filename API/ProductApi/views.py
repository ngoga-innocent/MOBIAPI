from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product, Categories, Shop, Color, Test, UserProfile, OurAdds, Comment, Notification, Rating, Like, UserFollow, UserLike, shopFollowers
from django.contrib.auth.models import User
from .serializer import ProductSerializer, ShopFollowersSerializer, NotificationSerializer, OurAddsSerializer, CategoriesSerializer, FollowersSerializer, ShopSerializer, ColorSerializer, TestSerializer, UserRegistrationSerializer, UserProfileSerializer, CommentSerializer, RatingSerializer, LikeSerializer, UserLikeSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import filters
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.auth import AuthToken
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from rest_framework.generics import RetrieveAPIView
import requests
import json
from rest_framework.renderers import JSONRenderer
from django.views.decorators.csrf import csrf_exempt
import uuid


class ProductApi(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'shop__name',
                     'seller__username', 'category__name']


class ColorApi(viewsets.ModelViewSet):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer
    filter_backends = [filters.SearchFilter]


class CategoriesApi(viewsets.ModelViewSet):
    queryset = Categories.objects.filter(parent__isnull=True)
    serializer_class = CategoriesSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


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


class ProductCategoryApi(APIView):

    def get(self, request, id):
        products = Product.objects.filter(category=id)
        serializer = ProductSerializer(
            products, many=True, context={'request': request})
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

        user = serializer.save()

        _, token = AuthToken.objects.create(user)

        return Response({
            'user_info': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            },
            'token': token
        })


class Login(APIView):
    def post(self, request):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get('user')
        _, token = AuthToken.objects.create(user)

        return Response({
            'user_info': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            },
            'token': token
        }, status=200)


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
            return Response({'error': 'you are not logged in'}, status=400)


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
        return Response({
            'shop': {
                'shop_id': shop_info.get('id'),
                'shop_name': shop_info.get('name'),
                'shop_profile': shop_info.get('profile'),
                'shop_location': shop_info.get('location'),
                'shop_tel': shop_info.get('telephone')

            }
        }, status=status.HTTP_200_OK)


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
                    'shop_cover': shop_info.get('cover')

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
        queryset = shopFollowers.objects.filter(shopid=sid)
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
        queryset = shopFollowers.objects.filter(shopid=sid)
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


def AuthPayment(request):
    url = "https://payments.paypack.rw/api/auth/agents/authorize"

    payload = json.dumps({
        "client_id": "3282d7d6-151f-11ee-a49d-dead99b23929",
        "client_secret": "c4dcc4f37d3c74d3b58d6e2b893eee3eda39a3ee5e6b4b0d3255bfef95601890afd80709"
    })

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        # Replace <access_token> with the actual token value
        'Authorization': 'Bearer {access_token}'
    }

    response = requests.post(url, headers=headers, data=payload)

    return JsonResponse({'response': response.json()})
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
        'client_id': 'mobishop',
        'grant_type': 'client_credentials',
        'client_secret': '78fd0071-dc5a-40b0-9776-27b823aba954',
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
            'callbackUrl': 'https://ngoga.pythonanywhere.com/callback'
        }
        print(payer_telephone_number)

        # Send Payments
        send_payments_response = requests.post(
            'https://payments.api.oltranz.com/api/v2/payments/mobile/collections',
            data=json.dumps(payments),
            headers=headers
        )
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
@api_view(['POST'])
def callBack(request):
    data = request.data

    return Response({'message': data})
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
