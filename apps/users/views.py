import json

from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.backends import ModelBackend
from apps.users.models import UserProfile, EmailVerifyRecord, Banner
from apps.operation.models import UserCourse, UserMessage
from apps.operation.models import UserFavorite
from apps.course.models import Course, Teacher, CourseOrg
from apps.users.forms import LoginForm, UpdateImageForm
from apps.users.forms import RegisterForm, ActiveForm, ForgetForm, ModifyForm, UpdateInfoForm
from django.views.generic.base import View
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from pure_pagination import Paginator, PageNotAnInteger


from utils.mixin_util import LoginRequiredMixin
from utils.email_send import send_register_email


class IndexView(View):
    def get(self, request):
        user = request.user
        banners = Banner.objects.all().order_by('index')
        courses = Course.objects.all()[:6]
        banner_courses = Course.objects.filter(is_banner=True)[:3]
        orgs = CourseOrg.objects.all()[:15]
        return render(request, 'index.html', {
            'user': user,
            'banners': banners,
            'courses': courses,
            'banner_courses': banner_courses,
            'orgs': orgs,
        })


class LogOutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('index'))


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html', {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get('username', '')
            pass_word = request.POST.get('password', '')
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return render(request, 'login.html', {'msg': '用户名或者密码错误'})
        else:
            return render(request, 'login.html', {'login_form': login_form})


class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, "register.html", {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get("email", "")
            pass_word = request.POST.get("password", "")
            exist_user = UserProfile.objects.filter(Q(username=user_name) | Q(email=user_name))
            if exist_user:
                return render(request, "forgetpwd.html", {'msg': "用户已经存在,若是本人忘记密码，请找回密码"})
            # 实例化一个user_profile对象，将前台值存入
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False

            # 加密password进行保存
            user_profile.password = make_password(pass_word)
            user_profile.save()
            send_register_email(user_name, 'register')

            # 给用户发送消息
            user_msg = UserMessage(user=user_profile.id)
            user_msg.message = '欢迎注册孟哥个网站'
            user_msg.save()

            return render(request, "login.html", {'msg': "激活连接已发送，注意查收"})
        else:
            return render(request, "register.html", {
                "register_form": register_form})


class ActiveUserView(View):
    def get(self, request, active_code):
        all_record = EmailVerifyRecord.objects.filter(code=active_code)
        active_form = ActiveForm(request.GET)
        if all_record:
            for record in all_record:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
                return render(request, 'login.html', {'msg': '账户已激活，请登录！'})
        else:
            return render(request, 'register.html', {'msg': '您的激活链接无效', 'active_form': active_form})


class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetForm(request.GET)
        return render(request, 'forgetpwd.html', {'forget_form': forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email', '')
            send_register_email(email, 'forget')
            return render(request, 'forgetpwd.html', {'forget_form': forget_form, 'msg': '重置密码连接已发送，请注意查收！'})
        else:
            return render(request, 'forgetpwd.html', {'forget_form': forget_form})


class ResetView(View):
    def get(self, request, active_code):
        all_record = EmailVerifyRecord.objects.filter(code=active_code)
        if all_record:
            for record in all_record:
                email = record.email
                return render(request, 'password_reset.html', {'email': email})
        else:
            return render(request, 'forgetpwd.html', {'msg': '重置密码连接无效，请重新请求'})


class ModifyPwdView(View):
    def post(self, request):
        modify_form = ModifyForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            email = request.POST.get('email', '')
            if pwd1 != pwd2:
                return render(request, 'password_reset.html', {'email': email, 'modify_form': modify_form, 'msg': '两次密码不同，请修改！'})
            else:
                user = UserProfile.objects.get(email=email)
                user.password = make_password(pwd2)
                user.save()
                return render(request, 'login.html', {'msg': '密码修改成功，请登录'})
        else:
            email = request.POST.get('email', '')
            return render(request, 'password_reset.html', {'email': email, 'modify_form': modify_form})


class UserCenterInfoView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'usercenter-info.html', {
        })

    def post(self, request):
        update_info_form = UpdateInfoForm(request.POST, instance=request.user)
        if update_info_form.is_valid():
            update_info_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(update_info_form.errors), content_type='application/json')


# 个人中心修改信息
class UpdateImageView(LoginRequiredMixin, View):
    def post(self, request):
        image_form = UpdateImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')


class UpdatePwdView(LoginRequiredMixin, View):
    def post(self, request):
        modify_form = ModifyForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            if pwd1 != pwd2:
                return HttpResponse('{"status":"fail", "msg":"密码不一致"}', content_type='application/json')
            else:
                request.user.password = make_password(pwd2)
                request.user.save()
                return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')


class UpdateEmailView(LoginRequiredMixin, View):
    def get(self, request):
        email = request.GET.get('email', '')
        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email":"邮箱已存在"}', content_type='application/json')
        send_register_email(email, send_type='change')
        return HttpResponse('{"status":"success"}', content_type="application/json")

    def post(self, request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')
        exist_record = EmailVerifyRecord.objects.filter(email=email, code=code, send_type='change')
        if exist_record:
            request.user.email = email
            request.user.save()
            return HttpResponse(
                '{"status":"success"}',
                content_type='application/json')
        else:
            return HttpResponse(
                '{"email":"验证码无效"}',
                content_type='application/json')


class UserCenterCourseView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        user_courses = UserCourse.objects.filter(user=user)
        courses = [usercourse.course for usercourse in user_courses]
        return render(request, 'usercenter-mycourse.html', {
            'courses': courses,
        })


class UserCenterMsg(LoginRequiredMixin, View):
    def get(self, request):
        user_msgs = UserMessage.objects.filter(user=request.user.id)
        for user_msg in user_msgs:
            user_msg.has_read = True
            user_msg.save()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(user_msgs, 5, request=request)
        my_msgs = p.page(page)
        return render(request, 'usercenter-message.html', {
            'my_msgs': my_msgs,

        })


class UserCenterMyFavCou(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        user_favs = UserFavorite.objects.filter(user=user, fav_type=1)
        fav_courses_ids = [user_fav.fav_id for user_fav in user_favs]
        fav_courses = Course.objects.filter(id__in=fav_courses_ids)
        return render(request, 'usercenter-fav-course.html', {
            'fav_courses': fav_courses,
        })


class UserCenterMyFavTea(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        user_favs = UserFavorite.objects.filter(user=user, fav_type=3)
        fav_teachers_ids = [user_fav.fav_id for user_fav in user_favs]
        fav_teachers = Teacher.objects.filter(id__in=fav_teachers_ids)
        return render(request, 'usercenter-fav-teacher.html', {
            'fav_teachers': fav_teachers,
        })


class UserCenterMyFavOrg(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        user_favs = UserFavorite.objects.filter(user=user, fav_type=2)
        fav_org_ids = [user_fav.fav_id for user_fav in user_favs]
        fav_orgs = CourseOrg.objects.filter(id__in=fav_org_ids)
        return render(request, 'usercenter-fav-org.html', {
            'fav_orgs': fav_orgs,
        })


# def page_not_found(request):
#     from django.shortcuts import render_to_response
#     response = render_to_response('404.html', {})
#     response.status_code = 404
#     return response
