from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Count, Q
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now
from django.views.decorators.http import require_http_methods
from ipware import get_client_ip

from accounts.forms import CreateForm
from .forms import UpdateForm
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

    analytics_list = ShortURL.objects \
        .filter(short_path=URL.short_path) \
        .annotate(total=Count('visit')) \
        .annotate(total_mobile=Count('visit', filter=
                Q(
                    visit__is_mobile=True,
                ))) \
        .annotate(total_pc=Count('visit', filter=
                Q(
                    visit__is_pc=True,
                ))) \
        .annotate(month=Count('visit', filter=
                Q(
                    visit__visited_at__lte=now(),
                    visit__visited_at__gte=now() - timedelta(days=30)
                ))) \
        .annotate(month_mobile=Count('visit', filter=
                Q(
                    Q(visit__is_mobile=True),
                    visit__visited_at__lte=now(),
                    visit__visited_at__gte=now() - timedelta(days=30)
                ))) \
        .annotate(month_pc=Count('visit', filter=
                Q(
                    Q(visit__is_pc=True),
                    visit__visited_at__lte=now(),
                    visit__visited_at__gte=now() - timedelta(days=30)
                ))) \
        .annotate(week=Count('visit', filter=
                Q(
                    visit__visited_at__lte=now(),
                    visit__visited_at__gte=now() - timedelta(days=7)
                ))) \
        .annotate(week_mobile=Count('visit', filter=
                Q(
                    Q(visit__is_mobile=True),
                    visit__visited_at__lte=now(),
                    visit__visited_at__gte=now() - timedelta(days=7)
                ))) \
        .annotate(week_pc=Count('visit', filter=
                Q(
                    Q(visit__is_pc=True),
                    visit__visited_at__lte=now(),
                    visit__visited_at__gte=now() - timedelta(days=7)
                ))) \
        .annotate(day=Count('visit', filter=
                Q(
                    visit__visited_at__lte=now(),
                    visit__visited_at__gte=now() - timedelta(days=1)
                ))) \
        .annotate(day_mobile=Count('visit', filter=
                Q(
                    Q(visit__is_mobile=True),
                    visit__visited_at__lte=now(),
                    visit__visited_at__gte=now() - timedelta(days=1)
                ))) \
        .annotate(day_pc=Count('visit', filter=
                Q(
                    Q(visit__is_pc=True),
                    visit__visited_at__lte=now(),
                    visit__visited_at__gte=now() - timedelta(days=1)
                ))) \
        .annotate(unique_total=Count('visit__ip', distinct=True)) \
        .annotate(unique_total_mobile=Count('visit__ip', filter=
                Q(
                    visit__is_mobile=True
                ), distinct=True)) \
        .annotate(unique_total_pc=Count('visit__ip', filter=
                Q(
                    visit__is_pc=True
                ), distinct=True)) \
        .annotate(unique_month=Count('visit__ip', filter=
                Q(
                    visit__visited_at__lte=now(),
                    visit__visited_at__gte=now() - timedelta(days=30)
                ), distinct=True))  \
        .annotate(unique_month_mobile=Count('visit__ip', filter=
                Q(
                    Q(visit__is_mobile=True),
                    visit__visited_at__lte=now(),
                    visit__visited_at__gte=now() - timedelta(days=30)
                ), distinct=True)) \
        .annotate(unique_month_pc=Count('visit__ip', filter=
                Q(
                    Q(visit__is_pc=True),
                    visit__visited_at__lte=now(),
                    visit__visited_at__gte=now() - timedelta(days=30)
                ), distinct=True)) \
        .annotate(unique_week=Count('visit__ip', filter=
                Q(
                    visit__visited_at__lte=now(),
                    visit__visited_at__gte=now() - timedelta(days=7)
                ), distinct=True))  \
        .annotate(unique_week_mobile=Count('visit__ip', filter=
                Q(
                    Q(visit__is_mobile=True),
                    visit__visited_at__lte=now(),
                    visit__visited_at__gte=now() - timedelta(days=7)
                ), distinct=True)) \
        .annotate(unique_week_pc=Count('visit__ip', filter=
                Q(
                    Q(visit__is_pc=True),
                    visit__visited_at__lte=now(),
                    visit__visited_at__gte=now() - timedelta(days=7)
                ), distinct=True)) \
        .annotate(unique_day=Count('visit__ip', filter=
                Q(
                    visit__visited_at__lte=now(),
                    visit__visited_at__gte=now() - timedelta(days=1)
                ), distinct=True))  \
        .annotate(unique_day_mobile=Count('visit__ip', filter=
                Q(
                    Q(visit__is_mobile=True),
                    visit__visited_at__lte=now(),
                    visit__visited_at__gte=now() - timedelta(days=1)
                ), distinct=True))  \
        .annotate(unique_day_pc=Count('visit__ip', filter=
                Q(
                    Q(visit__is_pc=True),
                    visit__visited_at__lte=now(),
                    visit__visited_at__gte=now() - timedelta(days=1)
                ), distinct=True)) \
        .distinct()

    return render(request, 'analytics/index.html', {
        'analytics': analytics_list,
    })


@login_required
def update(request, short_path):

    print(short_path)

    if request.method == 'POST':
        form = UpdateForm(request.POST)
        if form.is_valid():
            URL = ShortURL.objects.filter(short_path=short_path)

            new_short_path = form.cleaned_data['new_short_path']

            if not len(new_short_path):
                new_short_path = short_path

            URL.update(
                title=form.cleaned_data['title'],
                url=form.cleaned_data['url'],
                short_path=new_short_path,
                description=form.cleaned_data['description'],
            )
            messages.success(request, _('URL updated'))
            return redirect('dashboard')

    URL = ShortURL.objects.get(short_path=short_path)
    form = UpdateForm(initial={
        'title': URL.title,
        'url': URL.url,
        'current_short_path': URL.short_path,
        'description': URL.description,
    })
    return render(request, 'analytics/update.html', {'form': form})


@login_required
@require_http_methods(['POST'])
def delete(request, short_path):
    url = ShortURL.objects.filter(short_path=short_path)
    url.delete()
    messages.success(request, _('URL deleted!'))
    return redirect('dashboard')
