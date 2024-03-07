from django.forms import ModelForm
from django.urls import reverse_lazy

from web_app.forms import css_classes
from web_app.forms.widgets import ToggleWidget, SenderToggle
from web_app.models import Sender
from django import forms
from django.utils.translation import gettext_lazy as _


class SenderCreateForm(ModelForm):
    contact_id = forms.CharField(required=False, widget=forms.HiddenInput())
    email = forms.EmailField(
        required=False,

        widget=forms.TextInput(attrs={'placeholder': _('Type to search contacts'),
                                      'hx-trigger': 'input changed delay:500ms, search',
                                      'hx-indicator': '#loading-indicator-contacts-search',
                                      'hx-target': '#search-contacts-results-container',
                                      'hx-params': 'email',
                                      'type': 'search',
                                      'hx-swap':'innerHTML',
                                      'class': css_classes.search_input,
                                      'autocomplete': 'off'}),
        help_text=_("Type the company name to search for it."))
    is_active = forms.BooleanField(
        required=False,
        widget=SenderToggle()
    )

    class Meta:
        model = Sender
        fields = ['email', 'contact_id','is_active']

    def __init__(self, *args, **kwargs):
        self.organization = kwargs.pop('organization')
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['hx-post'] = reverse_lazy('search_contacts',
                                                                    kwargs={'organization_uuid': self.organization.pk})
