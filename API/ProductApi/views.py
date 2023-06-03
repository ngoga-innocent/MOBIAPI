from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product, Categories, Shop, Color, Test, UserProfile, Comment, Rating, Like, UserFollow, UserLike, shopFollowers
from django.contrib.auth.models import User
from .serializer import ProductSerializer, ShopFollowersSerializer, CategoriesSerializer, FollowersSerializer, ShopSerializer, ColorSerializer, TestSerializer, UserRegistrationSerializer, UserProfileSerializer, CommentSerializer, RatingSerializer, LikeSerializer, UserLikeSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import filters
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.auth import AuthToken
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from rest_framework.generics import RetrieveAPIView


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


class User(APIView):
    def get(self, request):
        user = request.user

        if user.is_authenticated:
            return Response({
                'user_info': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email
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
                    'shop_tel': shop_info.get('telephone')

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
            return Response({'msg': 'not followed'})

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
                return Response({'msg': 'updated'})
            else:
                return Response(serializer.errors, status=400)
        else:
            serializer = ShopFollowersSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'msg': 'created'})
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

# # Create your views here.
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
