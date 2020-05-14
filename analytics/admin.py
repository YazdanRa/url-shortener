from django.contrib import admin

from analytics import models
from analytics.models import Browser


class ShortURL(admin.ModelAdmin):
    list_display = ('id', 'title', 'short_path', 'created_at', 'updated_at')
    list_display_links = ('id', 'title', 'short_path')
    list_filter = ('updated_at', 'created_at')
    search_fields = ('id', 'title', 'short_path', 'url', 'description')


class Visit(admin.ModelAdmin):
    list_display = ('id', 'url', 'ip', 'browser', 'device', 'os', 'visited_at')
    list_display_links = ('id', 'url')
    list_filter = ('visited_at', 'is_routable', 'is_mobile', 'is_pc', 'is_tablet', 'is_touch_capable', 'is_bot')
    search_fields = ('id', 'url', 'ip')

    def browser(self, objects):
        return objects

    def device(self, objects):
        return objects

    def os(self, objects):
        return objects


admin.site.register(models.ShortURL, ShortURL)
admin.site.register(models.Visit, Visit)
