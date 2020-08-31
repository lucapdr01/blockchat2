"""socialDex URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from register import views as v
from api import views

urlpatterns = [

    path('admin/', admin.site.urls),
    path('register/', v.register, name="register"),
    path('logout/', v.logoutReq, name="logout"),
    path('login/', v.loginReq, name="login"),
    path('', include("api.urls")),
    path('', include("django.contrib.auth.urls")),
    path('posts/', views.posts),
    path('wordCheck', views.wordCheck),
    path('postList', views.postList, name="feed"),
    path('analytics', views.analytics, name="analytics"),
    path('user/<int:_id>/', views.userId, name='user_id'),
]
