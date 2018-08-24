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
from django.urls import path, include, re_path
import xadmin

from apps.users.views import IndexView, LoginView, RegisterView, ActiveUserView, ForgetPwdView, ResetView, ModifyPwdView
from apps.users.views import LogOutView
from django.views.static import serve
from mydjango1.settings import MEDIA_ROOT

urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogOutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path("captcha/", include('captcha.urls')),
    # 激活用户url
    re_path('active/(?P<active_code>.*)/', ActiveUserView.as_view(), name='user_active'),
    # 忘记密码
    path('forget/', ForgetPwdView.as_view(), name='forget_pwd'),
    re_path('reset/(?P<active_code>.*)/', ResetView.as_view(), name='reset_pwd'),
    path('modify_pwd/', ModifyPwdView.as_view(), name='modify_pwd'),

    # 课程机构
    path('org/', include('oragnization.urls', namespace='org')),
    # 公开课
    path('cou/', include('course.urls', namespace='cou')),
    # 用户中心
    path('user/', include('users.urls', namespace='user')),

    # 访问静态文件的处理view
    re_path('media/(?P<path>.*)', serve, {'document_root': MEDIA_ROOT}),
    # re_path('static/(?P<path>.*)', serve, {'document_root': STATIC_ROOT}),
]

# handler404 = 'users.views.page_not_found'
