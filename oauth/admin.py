from django.contrib import admin
from .models import OAuth_ex, OAuth_type


class OAuthTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type_name', 'title', 'img')


class OAuthAdmin(admin.ModelAdmin):
    list_display = ('id', 'account', 'openid', 'oauth_type')


admin.site.register(OAuth_ex, OAuthAdmin)
admin.site.register(OAuth_type, OAuthTypeAdmin)