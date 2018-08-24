from django import forms
from captcha.fields import CaptchaField
from apps.users.models import UserProfile


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)


class RegisterForm(forms.Form):
    # 此处email与前端name需保持一致。
    email = forms.EmailField(required=True)
    # 密码不能小于5位
    password = forms.CharField(required=True, min_length=5)
    # 应用验证码
    captcha = CaptchaField(error_messages={"invalid": u"验证码错误"})


class ActiveForm(forms.Form):
    captcha = CaptchaField(error_messages={"invalid": u"验证码错误"})


class ForgetForm(forms.Form):
    email = forms.EmailField(required=True)

    captcha = CaptchaField(error_messages={"invalid": u"验证码错误"})


class ModifyForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=5)
    password2 = forms.CharField(required=True, min_length=5)


class UpdateImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields =['image']


class UpdateInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields =['nick_name', 'birday', 'gender', 'address', 'mobile']