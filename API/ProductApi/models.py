from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Categories(models.Model):
    name=models.CharField(max_length=255)
    def __str__(self):
        return self.name
    
class Shop(models.Model):
    name=models.CharField(max_length=255,unique=True)
    profile=models.ImageField(blank=True)
    telephone=models.IntegerField()
    location=models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Product(models.Model):
    title=models.CharField(max_length=255)
    description=models.TextField()
    price=models.FloatField()
    rating=models.IntegerField()
    brand=models.CharField(max_length=255)
    category=models.ForeignKey(Categories,on_delete=models.CASCADE,related_name='category_name')
    thumbnail=models.ImageField(blank=True)
    images=models.ImageField(blank=True,null=True)
    seller=models.ForeignKey(User,on_delete=models.CASCADE,related_name='seller_name',null=True,blank=True)
    shop=models.ForeignKey(Shop,on_delete=models.CASCADE,null=True,blank=True,related_name='shop_name')

    def __str__(self):
        return self.title