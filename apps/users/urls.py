__author__ = "xumeng"
__date__ = "2018/8/17 15:03"
"""mydjango1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.core.urlresolvers import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from apps.users.views import UserCenterInfoView, UpdateImageView, UpdatePwdView, UpdateEmailView, UserCenterCourseView
from apps.users.views import UserCenterMsg, UserCenterMyFavOrg, UserCenterMyFavTea, UserCenterMyFavCou


app_name = 'users'
urlpatterns = [
    path('info/', UserCenterInfoView.as_view(), name='info'),
    path('image/update', UpdateImageView.as_view(), name='image_update'),
    path('update/pwd', UpdatePwdView.as_view(), name='update_pwd'),
    path('update/email', UpdateEmailView.as_view(), name='update_email'),
    path('course', UserCenterCourseView.as_view(), name='my_course'),
    path('message', UserCenterMsg.as_view(), name='my_msg'),
    path('fav/org', UserCenterMyFavOrg.as_view(), name='my_fav_org'),
    path('fav/cou', UserCenterMyFavCou.as_view(), name='my_fav_cou'),
    path('fav/tea', UserCenterMyFavTea.as_view(), name='my_fav_tea'),




]
