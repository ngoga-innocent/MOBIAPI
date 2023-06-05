from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Categories(models.Model):

    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='Categories', null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
#

    def __str__(self):
        return self.name


class Shop(models.Model):
    email = models.CharField(max_length=255, null=True, default='')
    name = models.CharField(max_length=255, unique=True)
    profile = models.ImageField(blank=True, upload_to='ShopProfile')
    cover = models.ImageField(blank=True, upload_to='ShopCover', null=True)
    telephone = models.IntegerField()
    location = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    password = models.CharField(max_length=255, default='Ngoga')

    def __str__(self):
        return self.name


class Color(models.Model):

    name = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):

    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.FloatField()
    rating = models.IntegerField()
    brand = models.CharField(max_length=255)
    category = models.ForeignKey(
        Categories, on_delete=models.CASCADE, related_name='category_name')
    thumbnail = models.ImageField(blank=True, upload_to='Thumbnail')
    images = models.ImageField(blank=True, null=True, upload_to='Images')
    seller = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='seller_name', null=True, blank=True)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE,
                             null=True, blank=True, related_name='shop_name')
    colors = models.ManyToManyField(Color, related_name='color')
    discount = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class ProductImages(models.Model):

    product = models.ForeignKey(
        Product, related_name='proimages', on_delete=models.CASCADE)
    Productimage = models.ImageField(upload_to='Images', blank=True)


class Test(models.Model):
    image = models.ImageField(upload_to='Test')


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models.CharField(max_length=255)
    profile = models.ImageField(upload_to='Profile')
    coverPhoto = models.ImageField(upload_to='Profile')
    library = models.ImageField(null=True, upload_to='Profile', blank=True)

    # def __str__(self):
    #     return self.user


class ProfileImages(models.Model):
    profile = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name='profileimages')
    images = models.ImageField(upload_to='Profile')


class Comment(models.Model):
    shopid = models.ForeignKey(Shop, on_delete=models.CASCADE)
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
    msg = models.TextField()


class Rating(models.Model):
    shopid = models.ForeignKey(Shop, on_delete=models.CASCADE)
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
    ratecount = models.TextField()


class Like(models.Model):
    shopid = models.ForeignKey(Shop, on_delete=models.CASCADE)

    like = models.IntegerField()
    dislike = models.IntegerField()


class UserLike(models.Model):
    shopid = models.ForeignKey(Shop, on_delete=models.CASCADE)
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
    liked = models.IntegerField(default=0)


class UserFollow(models.Model):
    shopid = models.ForeignKey(Shop, on_delete=models.CASCADE)
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
    followed = models.BooleanField()


class shopFollowers(models.Model):
    shopid = models.ForeignKey(Shop, on_delete=models.CASCADE)
    followers = models.IntegerField()


class Notification(models.Model):
    TYPE_CHOICE = [
        ('app notification', 'app notification'),
        ('other notification', 'other notification')
    ]
    type = models.CharField(choices=TYPE_CHOICE,
                            default='app notification', max_length=255)
    Notification = models.TextField()
