#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Huchong"
# Date: 2017/11/17
from django.forms import Form
from  django.forms import widgets
from django.forms import fields
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from app01 import models


class LoginForm(Form):
    username = fields.CharField(
        required=True,
        max_length=18,
        min_length=4,
        error_messages={
            'min_length': '不合要求，至少为4个字符',
            'max_length': '不合要求，至多为18个字符',
            'required': '用户名不能为空',

        },
        widget=widgets.TextInput(attrs={'placeholder': '用户名', 'class': 'form-control'}))
    password = fields.CharField(required=True,
                                error_messages={
                                    'required': '密码不能为空',
                                },
                                widget=widgets.TextInput(attrs={'placeholder': '密码', 'class': 'form-control'}))


class RegForm(Form):
    email = fields.EmailField(required=True,
                              error_messages={
                                  'required': '请输入邮箱地址',
                                  'invalid': '请输入正确的邮箱格式',
                              },
                              widget=widgets.TextInput(attrs={'placeholder': '需要通过邮件激活账户', 'class': 'form-control'}))
    # widget=widgets.TextInput(attrs={'placeholder': '需要通过邮件激活账户'})),
    tel = fields.IntegerField(required=True,
                              error_messages={
                                  'required': '请输入手机号码',
                              },
                              widget=widgets.TextInput(attrs={'placeholder': '激活帐户需要手机短信验证', 'class': 'form-control'}))

    username = fields.CharField(required=True,
                                max_length=18,
                                min_length=4,
                                error_messages={
                                    'required': '请输入登陆用户名',
                                    'min_length': '不合要求，至少为4个字符',
                                    'max_length': '不合要求，至多为18个字符',
                                },
                                widget=widgets.TextInput(
                                    attrs={'placeholder': '登录用户名，不少于4个字符', 'class': 'form-control'}))

    nickname = fields.CharField(required=True,
                                max_length=18,
                                min_length=4,
                                error_messages={
                                    'required': '请输入显示名称',
                                    'min_length': '不合要求，至少为4个字符',
                                    'max_length': '不合要求，至多为18个字符',
                                },
                                widget=widgets.TextInput(attrs={'placeholder': '即昵称，不少于2个字符', 'class': 'form-control'}))

    avatar = fields.FileField(required=False)

    password = fields.CharField(required=True,
                                min_length=8,
                                max_length=30,
                                error_messages={
                                    'required': '请输入密码',
                                    'min_length': '不合要求，密码长度要求8~30位',
                                    'max_length': '不合要求，密码长度要求8~30位'
                                },
                                widget=widgets.TextInput(
                                    attrs={'placeholder': '至少8位，必须包含字母、数字', 'class': 'form-control'}),
                                validators=[RegexValidator('\d+', '密码必须包含字母、数字的组合')]
                                )
    repeat_password = fields.CharField(required=True,
                                       error_messages={
                                           'required': '请输入确认密码'
                                       },
                                       widget=widgets.TextInput(
                                           attrs={'placeholder': '请输入确认密码', 'class': 'form-control'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        is_exsit = models.UserInfo.objects.filter(email=email)
        if is_exsit:
            raise ValidationError('邮箱已经存在！')
        else:
            return email

    def clean_username(self):
        user = self.cleaned_data['username']
        is_exsit = models.UserInfo.objects.filter(username=user)
        if is_exsit:
            raise ValidationError('登陆用户名已被使用！')
        else:
            return user

    def clean_nickname(self):
        nickname = self.cleaned_data['nickname']
        is_exsit = models.UserInfo.objects.filter(nickname=nickname)
        if is_exsit:
            raise ValidationError('显示名称已被使用！')
        else:
            return nickname

   
    def clean(self):
        password = self.cleaned_data.get('password')
        repeat_password = self.cleaned_data.get('repeat_password')
        if password != repeat_password:
            raise ValidationError('确认密码错误')
        else:
            return self.cleaned_data


from app01.plugins import xss_plugin


class ArticleForm(Form):
    title = fields.CharField(max_length=20, error_messages={
        "required": "不能为空",
    },)

    content = fields.CharField(error_messages={
        "required": "不能为空",
    }, widget=widgets.Textarea())

    def clean_content(self):
        html_str = self.cleaned_data.get("content")
        clean_content = xss_plugin.filter_xss(html_str)
        self.cleaned_data["content"] = clean_content

        return self.cleaned_data.get("content")
