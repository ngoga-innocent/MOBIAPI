from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Categories(models.Model):
    id = models.AutoField(primary_key=True)
    name=models.CharField(max_length=255)
    image=models.ImageField(upload_to='Categories',null=True)
    def __str__(self):
        return self.name
    
class Shop(models.Model):
    id = models.AutoField(primary_key=True)
    name=models.CharField(max_length=255,unique=True)
    profile=models.ImageField(blank=True)
    telephone=models.IntegerField()
    location=models.CharField(max_length=255)

    def __str__(self):
        return self.name
class Color(models.Model):
 
    name=models.CharField(max_length=1000,null=True)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    id = models.AutoField(primary_key=True)
    title=models.CharField(max_length=255)
    description=models.TextField()
    price=models.FloatField()
    rating=models.IntegerField()
    brand=models.CharField(max_length=255)
    category=models.ForeignKey(Categories,on_delete=models.CASCADE,related_name='category_name')
    thumbnail=models.ImageField(blank=True,upload_to='Thumbnail')
    images=models.ImageField(blank=True,null=True,upload_to='Images')
    seller=models.ForeignKey(User,on_delete=models.CASCADE,related_name='seller_name',null=True,blank=True)
    shop=models.ForeignKey(Shop,on_delete=models.CASCADE,null=True,blank=True,related_name='shop_name')
    colors=models.ManyToManyField(Color,null=True,related_name='color')
    def __str__(self):
        return self.title
class ProductImages(models.Model):
    id = models.AutoField(primary_key=True)
    product=models.ForeignKey(Product,related_name='proimages',on_delete=models.CASCADE)
    Productimage=models.ImageField(upload_to='Images',blank=True)
class Test(models.Model):
    image=models.ImageField(upload_to='Test')