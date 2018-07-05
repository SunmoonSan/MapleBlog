import redis
import markdown
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.urls import reverse
from django.views.generic import ListView
from django.conf import settings
from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseRedirect

from .models import Account, Article, Comment, ArticleLike, CommentLike, ArticleType


r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)


def home(request):
    try:
        is_login = request.session['is_login']
        if is_login:
            account = Account.objects.get(email=request.session['email'])

            articles = Article.objects.all()

            for article in articles:
                if r.get("article:{}:reads".format(article.id)) is not None:
                    article.read_count = r.get("article:{}:reads".format(article.id)).decode()
                else:
                    article.read_count = 0

            types = ArticleType.objects.all()
            for t in types:
                count = Article.objects.filter(articleType_id=t.id).count()
                t.count = count
            return render(request, 'blog/home.html', {
                'is_login': True,
                'user': account,
                'articles': articles,
                'types': types,
            })
    except KeyError:
        pass

    articles = Article.objects.all()

    for article in articles:
        if r.get("article:{}:reads".format(article.id)) is not None:
            article.read_count = r.get("article:{}:reads".format(article.id)).decode()
        else:
            article.read_count = 0

    types = ArticleType.objects.all()
    for t in types:
        count = Article.objects.filter(articleType_id=t.id).count()
        t.count = count
    return render(request, 'blog/home.html', {
        'is_login': False,
        'articles': articles,
        'types': types,
    })


def home_modify_intro(request):
    try:
        desc = request.POST['desc']
        print(desc)
        user = Account.objects.get(email=request.session['email'])
        user.intro = desc
        user.save()
        return HttpResponse("1")
    except (KeyError, Account.DoesNotExist):
        return HttpResponse("0")


def archive(request):

    obj_list = Article.objects.all()
    # create a paginator instance
    paginator = Paginator(obj_list, 5)

    # Get the page_number of current page
    current_page_num = request.GET.get('page')

    try:
        current_page = paginator.page(current_page_num)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        current_page = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        current_page = paginator.page(paginator.num_pages)

    article = current_page.object_list[0]
    print(type(article))
    for article in current_page.object_list:
        if r.get("article:{}:reads".format(article.id)) is not None:
            article.read_count = r.get("article:{}:reads".format(article.id)).decode()
        else:
            article.read_count = 0
    print(current_page.object_list[0])
    # print(current_page.object_list[1].title)
    return render(request, 'blog/archive.html',
                  {'current_page': current_page,
                   'paginator': paginator
                   })


def profile(request):
    if request.method == "POST":
        try:
            nickname = request.POST['nickname']
            phone = request.POST['phone']
            desc = request.POST['desc']

            account = Account.objects.get(email=request.session['email'])
            account.nickname = nickname
            account.phone = phone
            account.intro = desc
            account.save()
        except KeyError:
            raise KeyError

        return HttpResponse("修改成功")
    else:
        account = Account.objects.get(email=request.session['email'])
        return render(request, 'blog/profile.html', {
            'account': account,
        })


def my_image(request):
    if request.method == "POST":
        img = request.POST['img']
        account = Account.objects.get(email=request.session['email'])
        account.avatar = img
        account.save()
        return HttpResponse("1")
    else:
        return render(request, 'blog/imagecrop.html')


# 判断该邮箱是否已经注册过
def check_register_or_not(email):
    try:
        print('>>> ', email)
        account = Account.objects.get(email=email)
        # print('>>> ', str(account))
        is_exist = True
        return is_exist
    except Account.DoesNotExist:
        is_exist = False
        return is_exist


def result_message(request, title='Message', message='Unknown error, processing interrupted.'):
    return render(request, 'blog/result_message.html', {
        'title': title,
        'message': message,
    })


def do_sign_up(request, user_info):
    state = {
        'success': False,
        'message': '',
    }

    # 用户名不能为空
    if user_info['email'] == '':
        state['success'] = False
        state['message'] = 'username have not input.'
        return state

    # 密码不能为空
    if user_info['password'] == '':
        state['success'] = False
        state['message'] = 'password have not input'
        return state

    # 是否已经注册过
    if check_register_or_not(user_info['email']):
        state['success'] = False
        state['message'] = 'email have registered'
        return state

    # print(user_info['email'])
    # 判断两次输入密码是否相同
    if user_info['password'] != user_info['pwd_confirm']:
        state['success'] = False
        state['message'] = 'Confirm Password have not match.'
        return state

    account = Account(email=user_info['email'],
                      password=user_info['password']
                      )

    account.save()
    state['success'] = True
    state['message'] = 'Success'

    return state


#
# view method as following
#


# def blog_register(request):
#     """
#     注册
#     :param request:
#     :return:
#     """
#     if request.method == "GET":
#         register_form = RegisterForm()
#         return render(request, 'blog/blog_register.html', {'register_form': register_form})
#     else:
#         user_info = {
#             'email': '',
#             'password': '',
#             'pwd_confirm': '',
#         }
#
#         try:
#             user_info['email'] = request.POST['email']
#             user_info['password'] = request.POST['password']
#             user_info['pwd_confirm'] = request.POST['pwd_confirm']
#         except KeyError:
#             pass
#
#         state = do_sign_up(request, user_info)
#         if state['success']:
#             return result_message(request, title='Sign up success', message='your account was registered success.')
#             # return HttpResponseRedirect()
#
#         result = {
#             'success': state['success'],
#             'message': state['message'],
#             'form': {
#                 'email': user_info['email']
#             }
#         }
#
#         return render(request, 'blog/blog_register.html', {
#             'state': result,
#         })


# 判断是否登录
def __is_login(request):
    return request.session.get('is_login', False)


# 获取session用户名
def __get_username(request):
    return request.session.get('username', '')


# 获取session邮箱
def __get_email(request):
    return request.session.get('email', '')


def register(request):
    # is_login = __is_login(request)
    # if is_login:
    #     return HttpResponseRedirect('/')

    if request.method == 'POST':

        user_info = {
            'email': '',
            'password': '',
            'pwd_confirm': '',
        }

        try:
            user_info['email'] = request.POST['email']
            user_info['password'] = request.POST['password']
            user_info['pwd_confirm'] = request.POST['pwd_confirm']
        except KeyError:
            pass

        state = do_sign_up(request, user_info)
        if state['success']:
            return HttpResponseRedirect(reverse('blog:blog_login'))
            # return result_message(request, title='Sign up success', message='your account was registered success.')

    return render(request, 'blog/blog_register.html')


def check_login(email, password):
    state = {
        'success': True,
        'message': 'none',
    }

    try:
        account = Account.objects.get(email=email)

        if account.password == password:
            state['success'] = True
        else:
            state['success'] = False
            state['message'] = 'Password incorrect.'

    except Account.DoesNotExist:
        state['success'] = False
        state['message'] = 'User does not exist.'

    return state


def do_sign_in(request, email, password):
    state = check_login(email, password)

    if state['success']:
        request.session['is_login'] = True
        request.session['email'] = email

    return state


# def blog_login(request):
#     """
#     登录
#     :param request:
#     :return:
#     """
#     try:
#         email = request.POST['email']
#         password = request.POST['password']
#         print(email, password)
#         is_post = True
#     except KeyError:
#         is_post = False
#
#     if is_post:
#         state = do_sign_in(request, email, password)
#
#         if state['success']:
#             return render(request, 'blog/home.html')
#     state = {
#         'success': False,
#         'message': 'Please login first.'
#     }
#
#     return render(request, 'blog/blog_login.html', {
#         'state': state,
#     })


def login(request):
    if request.method == 'POST':
        try:
            email = request.POST['email']
            password = request.POST['password']
            state = do_sign_in(request, email, password)
            if state['success']:
                account = Account.objects.get(email=request.session['email'])

                articles = Article.objects.all()

                for article in articles:
                    if r.get("article:{}:reads".format(article.id)) is not None:
                        article.read_count = r.get("article:{}:reads".format(article.id)).decode()
                    else:
                        article.read_count = 0

                types = ArticleType.objects.all()
                for t in types:
                    count = Article.objects.filter(articleType_id=t.id).count()
                    t.count = count
                return render(request, 'blog/home.html', {
                    'is_login': True,
                    'user': account,
                    'articles': articles,
                    'types': types,
                })
        except KeyError:
            pass
    return render(request, 'blog/blog_login.html')


# def blog_logout(request):
#     request.session['is_login'] = False
#     request.session['email'] = ''
#     return HttpResponseRedirect('/')


def logout(request):
    request.session['is_login'] = ''
    request.session['email'] = ''

    articles = Article.objects.all()

    for article in articles:
        if r.get("article:{}:reads".format(article.id)) is not None:
            article.read_count = r.get("article:{}:reads".format(article.id)).decode()
        else:
            article.read_count = 0

    types = ArticleType.objects.all()
    for t in types:
        count = Article.objects.filter(articleType_id=t.id).count()
        t.count = count

    return HttpResponseRedirect(reverse('blog:home'))


# 发表博客
def do_save_blog(request, title, tag, content):
    print('>>> ', title, content)
    email = request.session['email']
    user = Account.objects.get(email=email)
    articleType = ArticleType(tag=tag)
    articleType.save()
    article = Article(title=title, articleType=articleType, content=content, author=user)
    article.save()


def blog_publish(request):
    if request.method == 'POST':
        title = ''
        articleType = ''
        content = ''
        try:
            title = request.POST['title']
            tag = request.POST['tag']
            content = request.POST['content']
            print(title, articleType, content)
            is_post = True
        except KeyError:
            is_post = False

        if is_post:
            do_save_blog(request, title, tag, content)
        else:
            pass
        return render(request, 'blog/home.html')
    else:
        print(request)
        return render(request, 'blog/blog_publish.html')


def blog_list(request):
    articles = Article.objects.all()
    print(articles)
    return render(request, 'blog/blog_list.html', {
        'articles': articles
    })


class BlogListView(ListView):
    model = Article
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        """
        在视图函数中将模板变量传递给模板是通过给 render 函数的 context 参数传递一个字典实现的，
        例如 render(request, 'blog/index.html', context={'post_list': post_list})，
        这里传递了一个 {'post_list': post_list} 字典给模板。
        在类视图中，这个需要传递的模板变量字典是通过 get_context_data 获得的，
        所以我们复写该方法，以便我们能够自己再插入一些我们自定义的模板变量进去。
        """

        # 首先获得父类生成的传递给模板的字典。
        context = super().get_context_data(**kwargs)

        # 父类生成的字典中已有 paginator、page_obj、is_paginated 这三个模板变量，
        # paginator 是 Paginator 的一个实例，
        # page_obj 是 Page 的一个实例，
        # is_paginated 是一个布尔变量，用于指示是否已分页。
        # 例如如果规定每页 10 个数据，而本身只有 5 个数据，其实就用不着分页，此时 is_paginated=False。
        # 关于什么是 Paginator，Page 类在 Django Pagination 简单分页：http://zmrenwu.com/post/34/ 中已有详细说明。
        # 由于 context 是一个字典，所以调用 get 方法从中取出某个键对应的值。
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')

        # 调用自己写的 pagination_data 方法获得显示分页导航条需要的数据，见下方。
        pagination_data = self.pagination_data(paginator, page, is_paginated)

        # 将分页导航条的模板变量更新到 context 中，注意 pagination_data 方法返回的也是一个字典。
        context.update(pagination_data)

        # 将更新后的 context 返回，以便 ListView 使用这个字典中的模板变量去渲染模板。
        # 注意此时 context 字典中已有了显示分页导航条所需的数据。
        return context

    def pagination_data(self, paginator, page, is_paginated):
        if not is_paginated:
            # 如果没有分页，则无需显示分页导航条，不用任何分页导航条的数据，因此返回一个空的字典
            return {}

        # 当前页左边连续的页码号，初始值为空
        left = []

        # 当前页右边连续的页码号，初始值为空
        right = []

        # 标示第 1 页页码后是否需要显示省略号
        left_has_more = False

        # 标示最后一页页码前是否需要显示省略号
        right_has_more = False

        # 标示是否需要显示第 1 页的页码号。
        # 因为如果当前页左边的连续页码号中已经含有第 1 页的页码号，此时就无需再显示第 1 页的页码号，
        # 其它情况下第一页的页码是始终需要显示的。
        # 初始值为 False
        first = False

        # 标示是否需要显示最后一页的页码号。
        # 需要此指示变量的理由和上面相同。
        last = False

        # 获得用户当前请求的页码号
        page_number = page.number

        # 获得分页后的总页数
        total_pages = paginator.num_pages

        # 获得整个分页页码列表，比如分了四页，那么就是 [1, 2, 3, 4]
        page_range = paginator.page_range

        if page_number == 1:
            # 如果用户请求的是第一页的数据，那么当前页左边的不需要数据，因此 left=[]（已默认为空）。
            # 此时只要获取当前页右边的连续页码号，
            # 比如分页页码列表是 [1, 2, 3, 4]，那么获取的就是 right = [2, 3]。
            # 注意这里只获取了当前页码后连续两个页码，你可以更改这个数字以获取更多页码。
            right = page_range[page_number:page_number + 2]

            # 如果最右边的页码号比最后一页的页码号减去 1 还要小，
            # 说明最右边的页码号和最后一页的页码号之间还有其它页码，因此需要显示省略号，通过 right_has_more 来指示。
            if right[-1] < total_pages - 1:
                right_has_more = True

            # 如果最右边的页码号比最后一页的页码号小，说明当前页右边的连续页码号中不包含最后一页的页码
            # 所以需要显示最后一页的页码号，通过 last 来指示
            if right[-1] < total_pages:
                last = True

        elif page_number == total_pages:
            # 如果用户请求的是最后一页的数据，那么当前页右边就不需要数据，因此 right=[]（已默认为空），
            # 此时只要获取当前页左边的连续页码号。
            # 比如分页页码列表是 [1, 2, 3, 4]，那么获取的就是 left = [2, 3]
            # 这里只获取了当前页码后连续两个页码，你可以更改这个数字以获取更多页码。
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]

            # 如果最左边的页码号比第 2 页页码号还大，
            # 说明最左边的页码号和第 1 页的页码号之间还有其它页码，因此需要显示省略号，通过 left_has_more 来指示。
            if left[0] > 2:
                left_has_more = True

            # 如果最左边的页码号比第 1 页的页码号大，说明当前页左边的连续页码号中不包含第一页的页码，
            # 所以需要显示第一页的页码号，通过 first 来指示
            if left[0] > 1:
                first = True
        else:
            # 用户请求的既不是最后一页，也不是第 1 页，则需要获取当前页左右两边的连续页码号，
            # 这里只获取了当前页码前后连续两个页码，你可以更改这个数字以获取更多页码。
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
            right = page_range[page_number:page_number + 2]

            # 是否需要显示最后一页和最后一页前的省略号
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True

            # 是否需要显示第 1 页和第 1 页后的省略号
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True

        data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
        }

        return data


def blog_detail(request, article_id):
    try:
        article = Article.objects.get(pk=article_id)
        comments = Comment.objects.filter(article_id=article_id, comment_type=True)

        for comment in comments:
            replies = Comment.objects.filter(comment_id=comment.id).order_by('ptime')
            comment.replies = replies

        read_count = r.incr("article:{}:reads".format(article.id))
        article.content = markdown.markdown(article.content,
                                            extensions={
                                                'markdown.extensions.extra',
                                                'markdown.extensions.codehilite',
                                                'markdown.extensions.toc'})
        return render(request, 'blog/blog_detail.html', {
            'article': article,
            'comments': comments,
            'read_count': read_count,
        })
    except:
        return HttpResponse("Detail")


# @csrf_exempt
# @require_POST
def blog_publish_comment(request):
    try:
        article_id = request.POST['article_id']
        article = Article.objects.get(id=article_id)
        comment_content = request.POST['comment']

        email = request.session['email']
        user = Account.objects.get(email=email)

        print('评论人', user.nickname)

        comment = Comment(comment_type=True, content=comment_content, article=article, fromUser=user)
        comment.save()
        print(article, comment_content)
        article.comment_set.add(comment)
        article.save()
        return HttpResponse("1")
    except Article.DoesNotExist:
        return HttpResponse("2")


def blog_like_article(request):
    # print(request.is_ajax())
    # print(article_id)
    try:
        article_id = request.POST['article_id']
        article = Article.objects.get(id=article_id)

        user = Account.objects.get(email=request.session['email'])
        like = ArticleLike(article=article, fromUser=user)
        like.save()
        return HttpResponse("1")
    except (KeyError, Account.DoesNotExist):
        return HttpResponse("0")


def blog_like_comment(request):
    try:
        comment_id = request.POST['comment_id']
        comment = Comment.objects.get(id=comment_id)

        user = Account.objects.get(email=request.session['email'])
        like = CommentLike(comment=comment, fromUser=user)
        like.save()
        return HttpResponse("1")
    except (Comment.DoesNotExist, KeyError):
        return HttpResponse("0")


# 回复评论
def blog_reply_comment(request):
    try:
        comment_id = request.POST['comment_id']
        content = request.POST['content']
        print(comment_id, content)

        c = Comment.objects.get(pk=comment_id)
        comment = Comment(article=c.article)
        comment.content = content
        comment.comment_type = False
        comment.comment_id = comment_id
        user = Account.objects.get(email=request.session['email'])
        print('回复评论', user.nickname)
        comment.fromUser = user
        comment.save()
        return HttpResponse("1")
    except (KeyError, Account.DoesNotExist):
        return HttpResponse("0")


# 回复回复
def blog_reply_reply(request):
    try:
        comment_id = request.POST['comment_id']
        to_uid = request.POST['to_uid']
        content = request.POST['content']

        print(comment_id, content)

        user = Account.objects.get(email=request.session['email'])  # 当前登录的User
        to_comment = Comment.objects.get(pk=to_uid)

        c = Comment.objects.get(pk=comment_id)
        comment = Comment(article=c.article, content=content, comment_type=False, fromUser=user, toUser=to_comment.fromUser)
        comment.comment_id = comment_id
        comment.save()
        return HttpResponse("1")
    except (KeyError, Account.DoesNotExist):
        return HttpResponse("0")