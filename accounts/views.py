from django.conf import settings
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError, PermissionDenied
from django.db.models import Count, Sum, Q, F, Max, DateTimeField
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods, require_POST, require_GET
from django.views.generic import ListView

from .forms import RegisterForm, LoginForm
from .models import CustomUser


@require_http_methods(['POST', 'GET'])
def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if not form.is_valid():
            return render(request, 'accounts/register.html', {'form': form})

        user = CustomUser.objects.create_user(
            username=form.cleaned_data['username'],
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password'],
        )

        messages.success(request, _('You have successfully registered!'))
        return redirect('login')
    else:
        form = RegisterForm()
        return render(request, 'accounts/register.html', {'form': form})


def login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():

            if '@' in form.cleaned_data['username']:
                user = auth.authenticate(email=form.cleaned_data['username'], password=form.cleaned_data['password'])
            else:
                user = auth.authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])

            if user is None:
                messages.error(request, _('Specifications entered are incorrect!'))
                return redirect('login')

            auth.login(request, user)
            messages.success(request, _('You have successfully logged in'))
            return redirect('dashboard')
        else:
            return render(request, 'accounts/login.html', {'form': form})
    else:
        form = LoginForm()
        return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, _('You have successfully logged out'))
        return redirect('index')


@login_required
def dashboard(request):
    pass
