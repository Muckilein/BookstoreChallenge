from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager

# Create your models here.


class CustomUser(AbstractUser):
    email=models.CharField(max_length=100,default=" ")   
    username=models.CharField(max_length=100,unique=True)
    author_pseudonym=models.CharField(max_length=100,default=" ")   
     

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []
  

    def __str__(self):
        return self.email
    

class Book(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True) 
    cover_image = models.ImageField(upload_to='cover_images/')
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title
