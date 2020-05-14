from django.contrib import admin

from accounts import models


class User(admin.ModelAdmin):
    list_display = ('id', 'username', 'email')
    list_display_links = ('id', 'username', 'email')
    search_fields = ('id', 'username', 'email')


admin.site.register(models.CustomUser, User)
