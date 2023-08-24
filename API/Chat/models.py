from django.db import models

# Create your models here.
class ChatAdmin(models.Model):
    username=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    status=models.BooleanField(default=False)
class Code(models.Model):
    user=models.ForeignKey(ChatAdmin,on_delete=models.CASCADE)
    code=models.IntegerField()    