#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @desc  : Created by San on 18-5-16 上午12:25
# @site  : https://github.com/SunmoonSan
import json
import urllib
import re


class OAuth_Base(object):    #基类，将相同的方法写入到此类中
    def __init__(self,client_id,client_key,redirect_url):   #初始化，载入对应的应用id、秘钥和回调地址
        self.client_id = client_id
        self.client_key = client_key
        self.redirect_url = redirect_url

    def _get(self,url,data):      # get方法
        request_url = '%s?%s' % (url,urllib.parse.urlencode(data))
        response = urllib.request.urlopen(request_url)
        return response.read()

    def _post(self,url,data):    # post方法
        request = urllib.request.Request(url,data = urllib.parse.urlencode(data).encode(encoding='UTF8'))     #1
        response = urllib.request.urlopen(request)
        return response.read()

# 下面的方法，不同的登录平台会有细微差别，需要继承基类后重写方法

    def get_auth_url(self):   # 获取code
        pass

    def get_access_token(self,code):   # 获取access token
        pass

    def get_open_id(self):    # 获取openid
        pass

    def get_user_info(self):   # 获取用户信息
        pass

    def get_email(self):   # 获取用户邮箱
        pass

# Github类
class OAuth_GITHUB(OAuth_Base):
    def get_auth_url(self):
        params = {
            'client_id':self.client_id,
            'response_type':'code',
            'redirect_uri':self.redirect_url,
            'scope':'user:email',
            'state':1
        }
        url = 'https://github.com/login/oauth/authorize?%s' % urllib.parse.urlencode(params)
        return url

    def get_access_token(self,code):
        params = {
            'grant_type':'authorization_code',
            'client_id':self.client_id,
            'client_secret':self.client_key,
            'code':code,
            'redirect_url':self.redirect_url
        }
        response = self._post('https://github.com/login/oauth/access_token',params)  #此处为post方法
        result = urllib.parse.parse_qs(response,True)
        self.access_token = result[b'access_token'][0]
        return self.access_token

#github不需要获取openid，因此不需要get_open_id()方法

    def get_user_info(self):
        params ={'access_token':self.access_token}
        response = self._get('https://api.github.com/user',params)
        result = json.loads(response.decode('utf-8'))
        self.openid = result.get('id','')
        return result

    def get_email(self):
        params ={'access_token':self.access_token}
        response = self._get('https://api.github.com/user/emails',params)
        result = json.loads(response.decode('utf-8'))
        return result[0]['email']