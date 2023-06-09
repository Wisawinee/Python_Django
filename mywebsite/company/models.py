from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    usertype = models.CharField(max_length=100, default='member')
    point = models.IntegerField(default=0)
    mobile = models.CharField(max_length=20,null=True,blank=True)

    def __str__(self):
        return self.user.username

class ResetPasswordToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username

'''
Product
    - title (Char)
    - description (Text)
    - price (decimal)
    - quantity (Int)
'''

class Product(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    quantity = models.IntegerField(default=1, null=True, blank=True)
    instock = models.BooleanField(default=True)

    def __str__(self):
        return self.title

'''
รัน 2 คำสั่งนี้ทุกครั้งที่มีการสร้าง model ใหม่หรือมีการเปลี่ยนแปลง
python manage.py makemigrations
python manage.py migrate
'''

class ContactList(models.Model):
    title = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    detail  = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False)

    def __str__(self):
        return self.title