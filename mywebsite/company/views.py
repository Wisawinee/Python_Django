from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *

#ระบบส่งไลน์
# from songline import Sendline # pip install songline

#ระบบส่งเมล์
from .emailsystem import sendthai

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

def Login(request):

    context  = {} #สิ่งที่จะแนบไป
    if request.method == 'POST':
        data = request.POST.copy()
        username = data.get('username')
        password = data.get('password')
        
        try:
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('profile-page')
        except:
            context['message'] = 'Username หรือ Password อาจไม่ถูกต้อง กรุณาลองใหม่อีกครั้ง'
    return render(request, 'company/login.html', context)

# def Home(request):
#     return HttpResponse('<h1>Hello World!</h1> <br> <p>by Sawinee</p>')

def Home(request):
    allproduct = Product.objects.all() # SELECT * from product
    context = {'allproduct':allproduct}
    return render(request, 'company/home.html', context)

def AboutUs(request):
    return render(request, 'company/aboutus.html')

def ContactUs(request):

    context  = {} #สิ่งที่จะแนบไป

    if request.method == 'POST':
        data = request.POST.copy()
        title = data.get('title')
        email = data.get('email')
        detail = data.get('detail')
        print(title)
        print(email)
        print(detail)
        print('----------------')

        # กรณีที่ user ไม่กรอกข้อมูล
        if title == '' and email == '':
            context['message'] = 'กรุณากรอกหัวข้อและอีเมลล์ เพราะจะส่งคำตอบให้ไม่ได้'
            return render(request, 'company/contact.html', context)

        # เมื่อได้ข้อมูลแล้วจะทำการบันทึกข้อมูล
        # ContactList(title=title,email=email,detail=detail).save()
        newrecord = ContactList()
        newrecord.title = title
        newrecord.email = email
        newrecord.detail = detail
        newrecord.save()
        context['message'] = 'ตอนนี้เรารับรับข้อมูลของคุณเรียบร้อยแล้ว รอตอบกลับภายใน 24 ชั่วโมง'

        #แจ้งอีเมลล์ตอบกลับ
        text = 'สวัสดีคุณลูกค้า\n\nทางเราได้รับปัญหาที่ท่านสอบถามเรียบร้อยแล้ว จะรีบติดต่อกลับโดยเร็วที่สุด'
        sendthai(email,'Wiz Company',text)


        # ส่งไลน์ from songline import Sendlinecmd
        # token = '1Zbjyzdhm1qlpbIgBMiEQNZaI9tt5Iiu0o5zJYd4xPC'
        # m = Sendline(token)
        # m.sendtext('\nหัวข้อ:{}\nอีเมลล์:{}\n>>>{}'.format(title,email,detail))

    return render(request, 'company/contact.html', context)

#from django.shortcuts import render, redirect
@login_required
def Accountant(request):
    #if request.user.profile.usertype != 'accountant':
    allow_user = ['accountant', 'admin']
    if request.user.profile.usertype not in allow_user:
        return redirect('home-page')
    #contact = ContactList.objects.all().order_by('-id')
    contact = ContactList.objects.all() # SELECT * from ContactList
    context = {'contact':contact}
    return render(request, 'company/accountant.html', context)

#from django.contrib.auth.models import User
def Register(request):

    context  = {} #สิ่งที่จะแนบไป

    if request.method == 'POST':
        data = request.POST.copy()
        fullname = data.get('fullname')
        mobile = data.get('mobile')
        username = data.get('username')
        password = data.get('password')
        password2 = data.get('password2')
        
        try:
            check =  User.objects.get(username=username)
            context['warning'] = 'email: {} มีในระบบแล้ว กรุณาใช้ email อื่นๆ'.format(username)
            context['fullname'] = fullname
            return render(request, 'company/register.html', context)
        except:
            if password != password2:
                context['warning'] = 'กรุณากรอกรหัสผ่านให้ถูกต้องทั้งสองช่อง'
                return render(request, 'company/register.html', context)

            newuser = User()
            newuser.username = username
            newuser.email = username
            newuser.first_name = fullname
            newuser.set_password(password)
            newuser.save()

            newprofile = Profile()
            newprofile.user = User.objects.get(username=username)
            newprofile.mobile = mobile
            newprofile.save()

        try:
            user = authenticate(username=username, password=password)
            login(request, user)
        except:
            context['message'] = 'Username หรือ Password อาจไม่ถูกต้อง กรุณาลองใหม่อีกครั้ง'
    return render(request, 'company/register.html', context)

@login_required
def ProfilePage(request):
    context = {}
    profileuser = Profile.objects.get(user=request.user)
    context['profile'] = profileuser
    return render(request, 'company/profile.html', context)

import uuid
def ResetPassword(request):

    context  = {} #สิ่งที่จะแนบไป
    if request.method == 'POST':
        data = request.POST.copy()
        username = data.get('username')

        try:
            user = User.objects.get(username=username)
            u = uuid.uuid1()
            token = str(u) #random uuid
            newreset = ResetPasswordToken()
            newreset.user = user
            newreset.token = token
            newreset.save()
            # sendthai(username,reset password link (Uncle Shop)', 'กรุณากดจากลิ้งค์นี้เพื่อ reset....')
            return redirect('home-page')
        except:
            context['message'] = 'email ของคุณไม่มีในระบบ กรุณาตรวจสอบความถูกต้องหรือสมัครสมาชิกใหม่'
    return render(request, 'company/resetpassword.html', context)