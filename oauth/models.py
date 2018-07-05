from django.db import models
from blog.models import Account


class OAuth_type(models.Model):
    type_name = models.CharField(max_length=12)
    title = models.CharField(max_length=12)
    img = models.FileField(upload_to='static/img/connect')

    def __str__(self):
        return self.type_name


class OAuth_ex(models.Model):
    account = models.ForeignKey(Account, on_delete=True)
    openid = models.CharField(max_length=64, default='')
    oauth_type = models.ForeignKey(OAuth_type, on_delete=True, default=1)

    def __str__(self):
        return '<%s>' % self.account
