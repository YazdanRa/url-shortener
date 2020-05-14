from django.contrib import admin

from analytics import models

admin.site.register(models.ShortURL)
admin.site.register(models.Visit)
admin.site.register(models.Device)
admin.site.register(models.OperationSystem)
admin.site.register(models.Browser)
