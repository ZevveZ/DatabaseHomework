# coding: utf-8
from django import forms
from django.contrib.auth.models import User

from .validation import validate


class ActivityForm(forms.Form):
    name = forms.CharField(label='社团名称', max_length=20)
    account = forms.EmailField(label='绑定邮箱')
    introduce = forms.CharField(label='社团简介', widget=forms.Textarea, max_length=200)
    password = forms.CharField(label='账号密码', widget=forms.PasswordInput, max_length=20)
    second_psd = forms.CharField(widget=forms.PasswordInput, max_length=20)

    def clean(self):
        cleaned_data = super(ActivityForm, self).clean()
        psd = cleaned_data.get('password')
        sec_psd = cleaned_data.get('second_psd')

        if psd != sec_psd:
            raise forms.ValidationError("两次密码输入不一致!", code='psd-inequality')

        # 验证社团名称是否已经注册过
        name = cleaned_data.get('name')
        try:
            User.objects.get(last_name=name)
        except User.DoesNotExist:
            pass
        else:
            raise forms.ValidationError("社团名称已经被注册！")

        # 验证邮箱是否已经注册过
        account = cleaned_data.get('account')
        try:
            User.objects.get(username=account)
        except User.DoesNotExist:
            pass
        else:
            raise forms.ValidationError("邮箱已被其他社团注册")


class PersonalForm(forms.Form):
    xuehao = forms.CharField(max_length=15)
    realname = forms.CharField(max_length=30)
    nickname = forms.CharField(max_length=10)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    sec_psd = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super(PersonalForm, self).clean()
        psd = cleaned_data.get('password')
        sec_psd = cleaned_data.get('sec_psd')

        if psd != sec_psd:
            raise forms.ValidationError("两次密码输入不一致!", code='psd-inequality')

        # 验证学号和姓名
        xh = cleaned_data.get('xuehao')
        xm = cleaned_data.get('realname')
        if not validate(xh, xm):
            raise forms.ValidationError("学号和姓名不一致！")

        # 验证学号是否已经注册过
        try:
            User.objects.get(username=xh)
        except User.DoesNotExist:
            pass
        else:
            raise forms.ValidationError("学号已经被注册！")


