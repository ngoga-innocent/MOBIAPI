from django.db import models
# from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.utils import timezone

# Create your models here.


class Categories(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='Categories', null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, phone_number, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(
            email=email, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("phone_number",'')

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser has to be have is_staff permissions")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(
                "Superuser has to be have is_superuser permissions")
        return self.create_user(email=email, password=password, **extra_fields)


class CustomUser(AbstractBaseUser):
    email = models.CharField(max_length=255, unique=True, null=True)
    username = models.CharField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=255,default='')
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    device_token=models.TextField(default='')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser


class VerificationCode(models.Model):
    code = models.CharField(max_length=15)
    created = models.DateTimeField(default=timezone.now)
    username = models.CharField(max_length=255)

    def __str__(self):
        return self.username


class ShopVerificationCode(models.Model):
    code = models.CharField(max_length=15)
    created = models.DateTimeField(default=timezone.now)
    name = models.CharField(max_length=255)


class Shop(models.Model):
    email = models.CharField(max_length=255, null=True, default='')
    name = models.CharField(max_length=255, unique=True)
    profile = models.ImageField(blank=True, upload_to='ShopProfile')
    cover = models.ImageField(blank=True, upload_to='ShopCover', null=True)
    telephone = models.IntegerField()
    location = models.CharField(max_length=255)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    password = models.CharField(max_length=255, default='Ngoga')
    idCard = models.ImageField(upload_to='Id')
    image = models.ImageField(upload_to='Owners')

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
        CustomUser, on_delete=models.CASCADE, related_name='seller_name', null=True, blank=True)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE,
                             default=None, null=True, related_name='shop_name')
    colors = models.ManyToManyField(Color, related_name='color')
    discount = models.IntegerField(default=0)
    name = models.CharField(max_length=255, null=True)
    phone = models.CharField(max_length=20, null=True)
    IdCard = models.ImageField(upload_to='Id', null=True)
    image = models.ImageField(upload_to='Id', null=True)
    created_at = models.DateTimeField(default=timezone.now)
    place=models.CharField(max_length=255,default='Normal')

    def __str__(self):
        return self.title


class ProductImages(models.Model):
    product = models.ForeignKey(
        Product, related_name='proimages', on_delete=models.CASCADE)
    Productimage = models.ImageField(upload_to='Images', blank=True)


class Test(models.Model):
    image = models.ImageField(upload_to='Test')


class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    about = models.CharField(max_length=255)
    profile = models.ImageField(upload_to='Profile')
    coverPhoto = models.ImageField(upload_to='Profile')
    library = models.ImageField(null=True, upload_to='Profile', blank=True)
    
    def __str__(self):
        return self.user

class ProfileImages(models.Model):
    profile = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name='profileimages')
    images = models.ImageField(upload_to='Profile')


class Comment(models.Model):
    shopid = models.ForeignKey(Shop, on_delete=models.CASCADE)
    userid = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    msg = models.TextField()


class Rating(models.Model):
    shopid = models.ForeignKey(Shop, on_delete=models.CASCADE)
    userid = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    ratecount = models.TextField()


class Like(models.Model):
    shopid = models.ForeignKey(Shop, on_delete=models.CASCADE)
    like = models.IntegerField()
    dislike = models.IntegerField()


class UserLike(models.Model):
    shopid = models.ForeignKey(Shop, on_delete=models.CASCADE)
    userid = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    liked = models.IntegerField(default=0)


class UserFollow(models.Model):
    shopid = models.ForeignKey(Shop, on_delete=models.CASCADE)
    userid = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    followed = models.BooleanField()


class ShopFollowers(models.Model):
    shopid = models.ForeignKey(Shop, on_delete=models.CASCADE)
    followers = models.IntegerField()


class Notification(models.Model):
    TYPE_CHOICE = [
        ('app notification', 'app notification'),
        ('other notification', 'other notification')
    ]
    name = models.CharField(max_length=255, default='Updates')
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    type = models.CharField(choices=TYPE_CHOICE,
                            default='app notification', max_length=255)
    message = models.TextField()
    
    def __str__(self):
        return self.name


class OurAdds(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='our Adds')
class Payment(models.Model):
    transId=models.CharField(max_length=255)
    telephone=models.CharField(max_length=255)
    amount=models.IntegerField()
    statusCode=models.IntegerField()
    status=models.CharField(max_length=255)
    trackId=models.CharField(max_length=255)
    description=models.TextField()

    def __str__(self):
        return self.transId

class FreeCredit(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    credits=models.IntegerField()
    def __str__(self):
        return self.user

class News(models.Model):
    title=models.CharField(max_length=255)
    subtitle=models.CharField(max_length=255,null=True)
    url=models.URLField()
    thumbnail=models.ImageField(upload_to='News',default='no Image')

    def __str__(self):
        return self.title
    
class Jobs(models.Model):
    title=models.CharField(max_length=255)
    description=models.TextField()
    contact=models.CharField(max_length=255)
    approved=models.BooleanField(default=False)
    owner=models.ForeignKey(CustomUser,on_delete=models.CASCADE,default=1)
    salary=models.IntegerField(default=0)

class DeviceTokens(models.Model):
    deviceToken=models.TextField()
    def __str__(self):
        return self.deviceToken