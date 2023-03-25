from django.contrib import admin
from .models import *

admin.site.register(Product) #เป็นการทำให้แอดมินสามารถเห็นฐานข้อมูล
admin.site.register(ContactList) #เพิ่ม Model ใหม่อีกรายการ
admin.site.register(Profile)
admin.site.register(ResetPasswordToken)
