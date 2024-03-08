from django import forms
from django.urls import reverse_lazy

from web_app.forms import css_classes
from web_app.forms.css_classes.inputs import text_input
from django.utils.translation import gettext_lazy as _

from web_app.forms.widgets import SearchContactWidget
from web_app.models import Company, Contact


class CompanyForm(forms.ModelForm):
    address = forms.CharField(label=_("Address"),
                              required=False,
                              widget=forms.TextInput(attrs={'placeholder': _('Address'), 'class': text_input}))
    reference_contact = forms.ModelChoiceField(
        queryset=Contact.objects.all(),
        widget=forms.HiddenInput(),
        required=False,
        label=_('Reference contact'),
        help_text=_("Select the reference contact for the company."))
    email = forms.EmailField(
        required=False,
        widget=SearchContactWidget(),
        help_text=_("Type to search for a contact."))

    class Meta:
        model = Company
        fields = ('reference_contact', 'address')

    def __init__(self, *args, **kwargs):
        self.organization = kwargs.pop('organization')
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['hx-post'] = reverse_lazy('search_contacts',
                                                                    kwargs={'organization_uuid': self.organization.pk})
        if self.instance is not None:
            self.fields['email'].initial = self.instance.reference_contact.email

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
