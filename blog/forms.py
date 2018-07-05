#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @desc  : Created by San on 18-4-11 下午9:06
# @site  : https://github.com/SunmoonSan
from django import forms
from django.contrib.auth.models import User

from .models import Account, Comment


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('phone',)


class RegisterForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    pwd_confirm = forms.CharField(label="Password again", widget=forms.PasswordInput)

    class Meta:
        model = User
        # account = Account
        # user.username
        # user.email
        # user.account
        fields = ('email',)

    # def clean_pwd_confirm(self):
    #     cd = self.cleaned_data
    #     if cd['password'] != cd['pwd_confirm']:
    #         raise forms.ValidationError("password do not match.")
    #     return cd['pwd_confirm']

