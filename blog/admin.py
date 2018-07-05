from django.contrib import admin
from .models import Account, ArticleType


class AccountAdmin(admin.ModelAdmin):
    list_display = ('email', 'nickname')


admin.site.register(Account, AccountAdmin)


class ArticleTypeAdmin(admin.ModelAdmin):
    list_display = ('tag',)


admin.site.register(ArticleType, ArticleTypeAdmin)
