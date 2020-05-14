from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods

from .models import ShortURL, Visit, Browser, OperationSystem, Device


@require_http_methods(['GET'])
def visit_record(request, short_path):
    URL = get_object_or_404(ShortURL, short_path=short_path)

    visit = Visit.objects.create(
        url=URL,
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
def analytics(request, short_path):
    URL = get_object_or_404(ShortURL, short_path=short_path)
    if URL.user.id != request.user.id:
        raise PermissionDenied
    return render(request, 'analytics/index.html')
