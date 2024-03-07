from django import forms
from django.urls import reverse_lazy

from web_app.forms import css_classes
from web_app.forms.css_classes.inputs import text_input
from django.utils.translation import gettext_lazy as _

from web_app.models import Company


class CompanyForm(forms.ModelForm):
    name = forms.CharField(label=_("Name"),
                           widget=forms.TextInput(attrs={'placeholder': _('Name'), 'class': text_input}))

    class Meta:
        model = Company
        fields = ('name',)


class CompanyUpdateForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': _('Untitled Space*'),
                                                         'class': css_classes.text_space_title_input,
                                                         'hx-trigger': 'blur changed'}),
                           label=_('Company title')
                           )

    class Meta:
        model = Company
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance is not None:
            self.fields['name'].widget.attrs['hx-post'] = reverse_lazy('company_update',
                                                                       kwargs={'company_uuid': self.instance.pk})
