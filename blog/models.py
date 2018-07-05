from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
    email = models.EmailField()
    phone = models.CharField(max_length=11, null=True, blank=True)
    password = models.CharField(max_length=100)
    intro = models.TextField()
    nickname = models.CharField(max_length=100, null=True, blank=True)
    avatar = models.ImageField(blank=True)

    def __str__(self):
        return self.nickname


class ArticleType(models.Model):
    tag = models.CharField(max_length=100)


class Article(models.Model):
    title = models.CharField(max_length=100)
    publish_time = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    author = models.ForeignKey(Account, on_delete=True)
    articleType = models.ForeignKey(ArticleType, on_delete=True, null=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.title


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=True)
    comment_type = models.BooleanField()
    comment_id = models.IntegerField(default=-1)
    content = models.TextField()
    fromUser = models.ForeignKey(Account, on_delete=True, related_name='comment_from_uid')
    toUser = models.ForeignKey(Account, on_delete=True, related_name='comment_to_uid', null=True)
    ptime = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-ptime',)


class CommentResult(Comment):
    class Meta:
        proxy = True


class ArticleLike(models.Model):
    article = models.ForeignKey(Article, on_delete=True)
    fromUser = models.ForeignKey(Account, on_delete=True, related_name='article_like_from_uid')


class CommentLike(models.Model):
    comment = models.ForeignKey(Comment, on_delete=True)
    fromUser = models.ForeignKey(Account, on_delete=True, related_name='comment_like_from_uid')
