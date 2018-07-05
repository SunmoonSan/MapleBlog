from django.shortcuts import render, render_to_response
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import OAuth_ex
from .oauth_client import OAuth_GITHUB

import time, uuid


def github_login(request):
    oauth_github = OAuth_GITHUB(settings.GITHUB_APP_ID, settings.GITHUB_KEY, settings.GITHUB_CALLBACK_URL)
    url = oauth_github.get_auth_url()
    print('>>> ', url)
    # return HttpResponseRedirect(url)
    return "http://www.baidu.com"


def github_check(request):
    type = '1'
    request_code = request.GET.get('code')
    oauth_git = OAuth_GITHUB(settings.GITHUB_APP_ID, settings.GITHUB_KEY, settings.GITHUB_CALLBACK_URL)
    try:
        access_token = oauth_git.get_access_token(request_code)  # 获取access token
        time.sleep(0.1)  # 此处需要休息一下，避免发送urlopen的10060错误
    except:  # 获取令牌失败，反馈失败信息
        data = {}
        data['goto_url'] = '/'
        data['goto_time'] = 10000
        data['goto_page'] = True
        data['message_title'] = '登录失败'
        data['message'] = '获取授权失败，请确认是否允许授权，并重试。若问题无法解决，请联系网站管理人员'
        return render_to_response('oauth/response.html', data)
    infos = oauth_git.get_user_info()  # 获取用户信息
    nickname = infos.get('login', '')
    image_url = infos.get('avatar_url', '')
    open_id = str(oauth_git.openid)
    signature = infos.get('bio', '')
    if not signature:
        signature = "无个性签名"
    sex = '1'
    githubs = OAuth_ex.objects.filter(openid=open_id, type=type)  # 查询是否该第三方账户已绑定本网站账号
    if githubs:  # 若已绑定，直接登录
        auth_login(request, githubs[0].user, backend='django.contrib.auth.backends.ModelBackend')
        return HttpResponseRedirect('/')
    else:  # 否则尝试获取用户邮箱用于绑定账号
        try:
            email = oauth_git.get_email()
        except:  # 若获取失败，则跳转到绑定用户界面，让用户手动输入邮箱
            url = "%s?nickname=%s&openid=%s&type=%s&signature=%s&image_url=%s&sex=%s" % (
            reverse('oauth:bind_email'), nickname, open_id, type, signature, image_url, sex)
            return HttpResponseRedirect(url)
    users = User.objects.filter(email=email)  # 若获取到邮箱，则查询是否存在本站用户
    if users:  # 若存在，则直接绑定
        user = users[0]
    else:  # 若不存在，则新建本站用户
        while User.objects.filter(username=nickname):  # 防止用户名重复
            nickname = nickname + '*'
        user = User(username=nickname, email=email, sex=sex, signature=signature)
        pwd = str(uuid.uuid1())  # 随机设置用户密码
        user.set_password(pwd)
        user.is_active = True
        user.download_image(image_url, nickname)  # 下载用户头像图片
        user.save()
    oauth_ex = OAuth_ex(user=user, openid=open_id, type=type)
    oauth_ex.save()  # 保存后登陆
    auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
    data = {}  # 反馈登陆结果
    data['goto_url'] = '/'
    data['goto_time'] = 10000
    data['goto_page'] = True
    data['message_title'] = '绑定用户成功'
    data['message'] = u'绑定成功！您的用户名为：<b>%s</b>。您现在可以同时使用本站账号和此第三方账号登录本站了！' % nickname
    return render_to_response('oauth/response.html', data)