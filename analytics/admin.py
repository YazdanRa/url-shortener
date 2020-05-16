from django.contrib import admin

from analytics import models
from analytics.models import Browser, Device, OperationSystem


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
        browser = Browser.objects.filter(url_visited=objects).get()
        return '{} ({})'.format(browser.family, browser.version)

    def device(self, objects):
        device = Device.objects.filter(url_visited=objects).get()
        return '{} ({})'.format(device.family, device.brand)

    def os(self, objects):
        os = OperationSystem.objects.filter(url_visited=objects).get()
        return '{} ({})'.format(os.family, os.version)


admin.site.register(models.ShortURL, ShortURL)
admin.site.register(models.Visit, Visit)
