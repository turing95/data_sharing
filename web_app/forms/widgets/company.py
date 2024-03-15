from django import forms

from web_app.forms import css_classes
from django.utils.translation import gettext_lazy as _


class SearchCompanyWidget(forms.widgets.TextInput):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attrs.update({'placeholder': _('Type to search companies'),
                           'hx-trigger': 'input changed delay:500ms, search, searchCompany from:body',
                           'hx-indicator': '#loading-indicator-companies-search',
                           'hx-target': '#search-companies-results-container',
                           'hx-params': 'search_company',
                           'class': css_classes.search_input,
                           'type': 'search',
                           'autocomplete': 'off'})
