import uuid

from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_http_methods

from analytics.models import ShortURL
from yektanet.settings import SHORT_URL_TEMPLATE
from .forms import RegisterForm, LoginForm, CreateForm
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
            email=form.cleaned_data['email'].lower(),
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

            username = form.cleaned_data['username'].lower()
            if '@' in username:
                try:
                    user = CustomUser.objects.get(email=username)
                    username = user.username
                except:
                    pass

            user = auth.authenticate(username=username, password=form.cleaned_data['password'])

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
        return redirect('register')


@login_required
def dashboard(request):
    URL = ShortURL.objects.filter(user=request.user).all()
    return render(request, 'accounts/dashboard.html', {
        'urls': URL,
        'url_template': SHORT_URL_TEMPLATE
    })


@login_required
def create(request):
    if request.method == 'POST':
        form = CreateForm(request.POST)
        if form.is_valid():
            short_path = form.cleaned_data['short_path']

            if not len(short_path):
                short_path = uuid.uuid4().hex[:8]

            short_url = ShortURL.objects.create(
                user=request.user,
                title=form.cleaned_data['title'],
                url=form.cleaned_data['url'],
                short_path=short_path,
                description=form.cleaned_data['description'],
            )

            messages.success(request, _('Shortcut Created!'))
            return redirect('dashboard')

    form = CreateForm()
    return render(request, 'accounts/create.html', {
        'form': form
    })
