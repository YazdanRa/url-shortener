from django import forms
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from analytics.models import ShortURL


class UpdateForm(forms.Form):
    title = forms.CharField(
        label=_('Title')
    )

    url = forms.URLField(
        label=_('URL')
    )

    current_short_path = forms.CharField(
        label=_('Current Short Path'),
        required=False,
        widget=forms.TextInput(attrs={'readonly': ''})
    )

    new_short_path = forms.CharField(
        label=_('New Short Path (Optional)'),
        required=False
    )

    description = forms.CharField(
        label=_('Description (Optional)'),
        widget=forms.Textarea,
        required=False
    )

    def clean(self):
        cleaned_data = super().clean()

        new_short_path = cleaned_data.get('new_short_path', None)

        if len(new_short_path) and ShortURL.objects.filter(Q(short_path__iexact=new_short_path)).exists():
            raise forms.ValidationError(_('This short_path already exists!'), code='invalid_unique_field')
        return cleaned_data
