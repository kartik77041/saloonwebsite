from email.mime import audio
from enum import auto
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class Profile(models.Model):
    user= models.OneToOneField(User,on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=10)
    
    def __str__(self):
        return self.user.username

class schedule_info(models.Model):
    fname = models.CharField(max_length=225)
    lname = models.CharField(max_length=225,default = None)
    date = models.DateTimeField(auto_now=False)
    phone_number =models.CharField(max_length=225)
    def __str__(self):
        return self.fname + " " + self.lname

class Comments(models.Model):
    sno= models.AutoField(primary_key=True)
    comment=models.TextField()
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    parent=models.ForeignKey('self',on_delete=models.CASCADE, null=True )
    timestamp= models.DateTimeField(default=now)
    
    def __str__(self):
        return self.comment[0:13] + "..." + "by" + " " + self.user.username
