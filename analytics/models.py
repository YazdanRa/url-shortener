from datetime import timedelta

from django.db import models
from django.db.models import Count, Q
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from accounts.models import CustomUser


class ShortURL(models.Model):
    user = models.ForeignKey(CustomUser, related_name='short_url', on_delete=models.CASCADE)
    title = models.CharField(_('Title'), max_length=32)
    url = models.URLField(_('URL'))
    short_path = models.CharField(_('Short Path'), max_length=32, unique=True)
    description = models.TextField(_('Description'), max_length=512, null=True, blank=True)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)

    @property
    def visit(self):
        visit = Visit.objects.filter(url=self)\
            .annotate(total=Count('ip'))\
            .annotate(total_mobile=Count('ip', filter=
                    Q(
                        is_mobile=True,
                    )))\
            .annotate(total_pc=Count('ip', filter=
                    Q(
                        is_pc=True
                    )))\
            .annotate(last_month=Count('ip', filter=
                    Q(
                        visited_at__lte=now(),
                        visited_at__gte=now() - timedelta(days=30)
                    )))\
            .annotate(last_month_mobile=Count('ip', filter=
                    Q(
                        Q(is_mobile=True),
                        visited_at__lte=now(),
                        visited_at__gte=now() - timedelta(days=30)
                    )))\
            .annotate(last_month_pc=Count('ip', filter=
                    Q(
                        Q(is_pc=True),
                        visited_at__lte=now(),
                        visited_at__gte=now() - timedelta(days=30)
                    )))\
            .annotate(last_week=Count('ip', filter=
                    Q(
                        visited_at__lte=now(),
                        visited_at__gte=now() - timedelta(days=7)
                    )))\
            .annotate(last_week_mobile=Count('ip', filter=
                    Q(
                        Q(is_mobile=True),
                        visited_at__lte=now(),
                        visited_at__gte=now() - timedelta(days=7)
                    )))\
            .annotate(last_week_pc=Count('ip', filter=
                    Q(
                        Q(is_pc=True),
                        visited_at__lte=now(),
                        visited_at__gte=now() - timedelta(days=7)
                    )))\
            .annotate(last_day=Count('ip', filter=
                    Q(
                        visited_at__lte=now(),
                        visited_at__gte=now() - timedelta(days=1)
                    )))\
            .annotate(last_day_mobile=Count('ip', filter=
                    Q(
                        Q(is_mobile=True),
                        visited_at__lte=now(),
                        visited_at__gte=now() - timedelta(days=1)
                    )))\
            .annotate(last_day_pc=Count('ip', filter=
                    Q(
                        Q(is_pc=True),
                        visited_at__lte=now(),
                        visited_at__gte=now() - timedelta(days=1)
                    )))\
            .distinct()
        return visit

    @property
    def unique_visit(self):
        unique_visit = Visit.objects.filter(url=self)\
            .annotate(total=Count('ip', distinct=True))\
            .annotate(total_mobile=Count('ip', filter=
                    Q(
                        is_mobile=True
                    ), distinct=True))\
            .annotate(total_pc=Count('ip', filter=
                    Q(
                        is_pc=True
                    ), distinct=True))\
            .annotate(last_month=Count('ip', filter=
                    Q(
                        visited_at__lte=now(),
                        visited_at__gte=now() - timedelta(days=30)
                    ), distinct=True))\
            .annotate(last_month_mobile=Count('ip', filter=
                    Q(
                        Q(is_mobile=True),
                        visited_at__lte=now(),
                        visited_at__gte=now() - timedelta(days=30)
                    ), distinct=True))\
            .annotate(last_month_pc=Count('ip', filter=
                    Q(
                        Q(is_pc=True),
                        visited_at__lte=now(),
                        visited_at__gte=now() - timedelta(days=30)
                    ), distinct=True))\
            .annotate(last_week=Count('ip', filter=
                    Q(
                        visited_at__lte=now(),
                        visited_at__gte=now() - timedelta(days=7)
                    ), distinct=True))\
            .annotate(last_week_mobile=Count('ip', filter=
                    Q(
                        Q(is_mobile=True),
                        visited_at__lte=now(),
                        visited_at__gte=now() - timedelta(days=7)
                    ), distinct=True))\
            .annotate(last_week_pc=Count('ip', filter=
                    Q(
                        Q(is_pc=True),
                        visited_at__lte=now(),
                        visited_at__gte=now() - timedelta(days=7)
                    ), distinct=True))\
            .annotate(last_day=Count('ip', filter=
                    Q(
                        visited_at__lte=now(),
                        visited_at__gte=now() - timedelta(days=1)
                    ), distinct=True))\
            .annotate(last_day_mobile=Count('ip', filter=
                    Q(
                        Q(is_mobile=True),
                        visited_at__lte=now(),
                        visited_at__gte=now() - timedelta(days=1)
                    ), distinct=True))\
            .annotate(last_day_pc=Count('ip', filter=
                    Q(
                        Q(is_pc=True),
                        visited_at__lte=now(),
                        visited_at__gte=now() - timedelta(days=1)
                    ), distinct=True))\
            .distinct()
        return unique_visit

    def __str__(self):
        return '{} ({})'.format(self.title, self.user)


class Visit(models.Model):
    url = models.ForeignKey(ShortURL, related_name='visit', on_delete=models.CASCADE)
    visited_at = models.DateTimeField(auto_now_add=True)

    ip = models.GenericIPAddressField(_('IP Address'), null=True)
    is_routable = models.BooleanField(null=True)

    is_touch_capable = models.BooleanField()
    is_mobile = models.BooleanField()
    is_tablet = models.BooleanField()
    is_pc = models.BooleanField()
    is_bot = models.BooleanField()

    @property
    def browser(self):
        browser = Browser.objects.filter(url_visited=self).all()
        return browser

    @property
    def os(self):
        os = OperationSystem.objects.filter(url_visited=self).all()
        return os

    @property
    def device(self):
        device = Device.objects.filter(url_visited=self).all()
        return device

    class Meta:
        ordering = ['-visited_at']

    def __str__(self):
        return '{}'.format(self.url)


class Browser(models.Model):
    family = models.CharField(max_length=64)
    version = models.CharField(max_length=64)
    url_visited = models.ForeignKey(Visit, related_name='browser', on_delete=models.CASCADE)

    def __str__(self):
        return '{} ({})'.format(self.family, self.version)


class OperationSystem(models.Model):
    family = models.CharField(max_length=64)
    version = models.CharField(max_length=64)
    url_visited = models.ForeignKey(Visit, related_name='os', on_delete=models.CASCADE)

    def __str__(self):
        return '{} ({})'.format(self.family, self.version)


class Device(models.Model):
    family = models.CharField(max_length=64)
    brand = models.CharField(max_length=32)
    model = models.CharField(max_length=32)
    url_visited = models.ForeignKey(Visit, related_name='device', on_delete=models.CASCADE)

    def __str__(self):
        return '{} ({})'.format(self.family, self.brand)
