import string

from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.validators import RegexValidator
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from accounts.models import CustomUser
from analytics.models import ShortURL


class RegisterForm(forms.Form):

    username = forms.CharField(
        label=_('Username'),
        max_length=100,
        validators=[RegexValidator(
            regex='^([a-zA-Z0-9_])+$',
            message=_(
                'Invalid Username! (username only can include a-z, A-Z, 0-9 and \'_\')')
        )]
    )

    email = forms.EmailField(
        label=_('Email')
    )

    password = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput())

    confirm_password = forms.CharField(
        label=_('Confirm Password'),
        widget=forms.PasswordInput())

    def clean_password(self):
        password = self.cleaned_data.get('password', None)
        if password:
            validate_password(password)

        return password

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password', None)
        confirm_password = cleaned_data.get('confirm_password', None)

        if (password and confirm_password) and password != confirm_password:
            raise forms.ValidationError(_('The Password entered do not match'), code='password_confirm_mismatch')

        if CustomUser.objects.filter(
                Q(email__iexact=cleaned_data.get('email', '')) |
                Q(username__iexact=cleaned_data.get('username', ''))).count() > 0:
            raise forms.ValidationError(_('This email/username already exists!'), code='invalid_unique_field')

        return cleaned_data


class LoginForm(forms.Form):

    username = forms.CharField(
        label=_('Username/Email')
    )

    password = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput()
    )


class CreateForm(forms.Form):
    title = forms.CharField(
        label=_('Title')
    )

    url = forms.URLField(
        label=_('URL')
    )

    short_path = forms.CharField(
        label=_('Short Path (Optional)'),
        required=False
    )

    description = forms.CharField(
        label=_('Description (Optional)'),
        widget=forms.Textarea,
        required=False
    )

    def clean(self):
        cleaned_data = super().clean()

        short_path = cleaned_data.get('short_path', None)

        if len(short_path) and ShortURL.objects.filter(Q(short_path__iexact=short_path)).exists():
            raise forms.ValidationError(_('This short_path already exists!'), code='invalid_unique_field')
        return cleaned_data
