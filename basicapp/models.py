from django.db import models

# Create your models here.

class userinfo(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    reg_no = models.CharField(max_length=100)
    room_no = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone_no = models.BigIntegerField()
    

class Bookings(models.Model):
    user=models.CharField(max_length=40)
    date=models.CharField(max_length=10)
    check=models.CharField(max_length=40)
    end=models.CharField(max_length=40)
    cht=models.CharField(max_length=40)

class contact_us(models.Model):
    name=models.CharField(max_length=40)
    email=models.CharField(max_length=75)
    subject=models.TextField()
    feed=models.TextField()