from django import forms

from web_app.forms import css_classes
from django.utils.translation import gettext_lazy as _


class SearchContactWidget(forms.widgets.TextInput):

    def __init__(self, *args, **kwargs):
        #pop sender id from kwars if present
        sender_uuid = kwargs.pop('sender_uuid', '')
        super().__init__(*args, **kwargs)
        self.attrs.update({'placeholder': _('Type to search contacts'),
                           'hx-trigger': 'input changed delay:500ms, search',
                           'hx-indicator': f'#loading-indicator-contacts-search-{sender_uuid}',
                           'hx-target': f'#search-contacts-results-container-{sender_uuid}',
                           'hx-params': 'email',
                           'type': 'search',
                           'hx-swap': 'innerHTML',
                           'class': css_classes.search_input,
                           'autocomplete': 'off'})