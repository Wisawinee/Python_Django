from django.urls import path
from .views import *

urlpatterns = [
    path('', Home, name='home-page'), #localhost:8000
    path('about/', AboutUs, name='about-page'), #localhost:8000/about/
    path('contact/', ContactUs, name='contact-page'), #localhost:8000/contact/
    path('accountant/', Accountant, name='accountant-page'),
    path('register/', Register, name='register-page'),
    path('profile/',ProfilePage,name='profile-page'),
    path('reset-password/', ResetPassword,name='reset-password'),
]