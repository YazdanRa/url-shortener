from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Count, Sum, Q, F, Max, DateTimeField
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import now
from django.views.decorators.http import require_http_methods
from ipware import get_client_ip

from .models import ShortURL, Visit, Browser, OperationSystem, Device


@require_http_methods(['GET'])
def visit_record(request, short_path):
    URL = get_object_or_404(ShortURL, short_path=short_path)
    client_ip, is_routable = get_client_ip(request)

    visit = Visit.objects.create(
        url=URL,
        ip=client_ip,
        is_routable=is_routable,
        is_touch_capable=request.user_agent.is_touch_capable,
        is_mobile=request.user_agent.is_mobile,
        is_tablet=request.user_agent.is_tablet,
        is_pc=request.user_agent.is_pc,
        is_bot=request.user_agent.is_bot,
    )

    browser = Browser.objects.create(
        url_visited=visit,
        family=request.user_agent.browser.family,
        version=request.user_agent.browser.version_string,
    )

    os = OperationSystem.objects.create(
        url_visited=visit,
        family=request.user_agent.os.family,
        version=request.user_agent.os.version_string,
    )

    device = Device.objects.create(
        url_visited=visit,
        family=request.user_agent.device.family,
        brand=request.user_agent.device.brand,
        model=request.user_agent.device.model,
    )

    return redirect(URL.url)


@login_required
@require_http_methods(['GET'])
def analytics(request, short_path):
    URL = get_object_or_404(ShortURL, short_path=short_path)
    if URL.user.id != request.user.id:
        raise PermissionDenied

    analytics_list = ShortURL.objects\
        .filter(short_path=URL.short_path)\
        .annotate(total_visit=Count('visit'))\
        .annotate(month_visit=Count('visit', filter=
                    Q(
                        visit__visited_at__lte=now(),
                        visit__visited_at__gte=now() - timedelta(days=30)
                    )))\
        .annotate(week_visit=Count('visit', filter=
                    Q(
                        visit__visited_at__lte=now(),
                        visit__visited_at__gte=now() - timedelta(days=7)
                    )))\
        .annotate(day_visit=Count('visit', filter=
                    Q(
                        visit__visited_at__lte=now(),
                        visit__visited_at__gte=now() - timedelta(days=1)
                    )))\
        .distinct()

    return render(request, 'analytics/index.html', {
        'analytics': analytics_list
    })
