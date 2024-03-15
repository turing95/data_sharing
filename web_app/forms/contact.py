from django import forms
from django.urls import reverse

from web_app.forms import css_classes
from web_app.forms.css_classes.inputs import text_input
from django.utils.translation import gettext_lazy as _

from web_app.forms.widgets import SearchCompanyWidget
from web_app.models import Contact, Company


class ContactForm(forms.ModelForm):
    first_name = forms.CharField(required=False, label=_("First name"),
                                 widget=forms.TextInput(attrs={'placeholder': _('First Name'), 'class': text_input}))
    last_name = forms.CharField(required=False, label=_("Last name"),
                                widget=forms.TextInput(attrs={'placeholder': _('Last Name'), 'class': text_input}))
    email = forms.EmailField(label=_("Email"),
                             widget=forms.EmailInput(attrs={'placeholder': _('Email*'), 'class': text_input}))
    phone = forms.CharField(label=_("Phone Number"),
                            required=False,
                            widget=forms.TextInput(attrs={'placeholder': _('Phone Number'), 'class': text_input}))

    company = forms.ModelChoiceField(
        queryset=Company.objects.all(),
        widget=forms.HiddenInput(),
        required=True,
        label=_('Company'),
        help_text=_("Select the company to which the space belongs."))
    search_company = forms.CharField(
        required=False,
        widget=SearchCompanyWidget(),
        help_text=_("Type the company name to search for it."))

    class Meta:
        model = Contact
        fields = ('first_name', 'last_name', 'email', 'phone', 'company')

    def __init__(self, *args, **kwargs):
        self.organization = kwargs.pop('organization', None)
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['search_company'].widget.attrs['hx-post'] = reverse('search_companies', kwargs={
            'organization_uuid': self.organization.pk})
        if self.instance.company:
            self.fields['search_company'].initial = self.instance.company.name

    def clean(self):
        cleaned_data = super().clean()
        search_company = cleaned_data.get('search_company', None)
        if search_company:
            company = cleaned_data.get('company', None)
            if company and company.name != search_company:
                self.add_error('search_company', _('Select a company from the list or leave blank.'))
        return cleaned_data
