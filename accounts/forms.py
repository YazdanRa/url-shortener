import string

from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.validators import RegexValidator
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from accounts.models import CustomUser
from payment.forms import IranianCreditCardField
from vpn.models import PlanVariation


class BaseForm(forms.Form):
    def __init__(self, default_class, placeholder, *args, **kwargs):
        super().__init__(*args, **kwargs)
        text_fields = filter(
            lambda s: isinstance(s, forms.Field),
            self.fields.values())
        for field in text_fields:
            c = ''
            try:
                c = field.widget.attrs['class']
            except KeyError:
                pass

            field.widget.attrs.update({'class': c + ' ' + default_class})

            if placeholder:
                field.widget.attrs.update({'placeholder': field.label})


class LowerField(forms.CharField):
    def __init__(self, *args, **kwargs):
        super(LowerField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        return super().to_python(value).lower()


class NameField(forms.CharField):
    def __init__(self, *args, **kwargs):
        super(NameField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        return string.capwords(super().to_python(value))


# Actual forms start here #

class RegisterForm(BaseForm):
    def __init__(self, *args, **kwargs):
        super().__init__('input100', True, *args, **kwargs)

    username = LowerField(
        label=_('Username'),
        max_length=100,
        validators=[RegexValidator(
            regex='^([a-zA-Z0-9_])+$',
            message=_(
                'Invalid Username! (username only can include a-z, A-Z, 0-9 and \'_\')')
        )]
    )

    email = forms.EmailField(
        label=_('email'))

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


class LoginForm(BaseForm):
    def __init__(self, *args, **kwargs):
        super().__init__('input100', True, *args, **kwargs)

    username = LowerField(
        label=_('Username/Email'))

    password = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput())
