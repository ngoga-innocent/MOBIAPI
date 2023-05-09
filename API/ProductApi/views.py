from django.shortcuts import render
from rest_framework.response import Response
from .models import Product,Categories,Shop
from .serializer import ProductSerializer,CategoriesSerializer,ShopSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import filters



class ProductApi(viewsets.ModelViewSet):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    filter_backends=[filters.SearchFilter]
    search_fields=['title','shop__name','seller__username','category__name']

class CategoriesApi(viewsets.ModelViewSet):
    queryset=Categories.objects.all()
    serializer_class=CategoriesSerializer
    filter_backends=[filters.SearchFilter]
    search_fields=['name']
class ShopApi(viewsets.ModelViewSet):
    queryset=Shop.objects.all()
    serializer_class=ShopSerializer
    filter_backends=[filters.SearchFilter]
    search_fields=['name']
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
