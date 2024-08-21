from django.urls import path
from .views import *
app_name = ("accounts")
urlpatterns = [
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', register, name='register')
]