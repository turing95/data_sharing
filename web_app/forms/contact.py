from django import forms
from django.urls import reverse

from web_app.forms import css_classes
from web_app.forms.css_classes.inputs import text_input
from django.utils.translation import gettext_lazy as _

from web_app.models import Contact, Company


class CompanyField(forms.CharField):

    def to_python(self, value):
        if not value:
            return None
        try:
            return Company.objects.get(pk=value)
        except Company.DoesNotExist:
            raise forms.ValidationError(_("Company not found."))

    def prepare_value(self, value):
        if isinstance(value, Company):
            return value.uuid
        return super().prepare_value(value)


class ContactForm(forms.ModelForm):
    first_name = forms.CharField(required=False, label=_("First name"),
                                 widget=forms.TextInput(attrs={'placeholder': _('First Name'), 'class': text_input}))
    last_name = forms.CharField(required=False, label=_("Last name"),
                                widget=forms.TextInput(attrs={'placeholder': _('Last Name'), 'class': text_input}))
    email = forms.EmailField(label=_("Email"),
                             widget=forms.EmailInput(attrs={'placeholder': _('Email*'), 'class': text_input}))
    phone = forms.EmailField(label=_("Phone Number"),
                            widget=forms.EmailInput(attrs={'placeholder': _('Phone Number'), 'class': text_input}))
    
    company = forms.ModelChoiceField(
        queryset=Company.objects.all(),
        widget=forms.HiddenInput(),
        required=True,
        label=_('Company'),
        help_text=_("Select the company to which the space belongs."))
    search_company = forms.CharField(
        required=False,

        widget=forms.TextInput(attrs={'placeholder': _('Type to search companies'),
                                      'hx-trigger': 'input changed delay:500ms, search',
                                      'hx-indicator': '#loading-indicator-companies-search',
                                      'hx-target': '#search-companies-results-container',
                                      'hx-params': 'search_company',
                                      'class': css_classes.search_input,
                                      'autocomplete': 'off'}),
        help_text=_("Type the company name to search for it."))

    class Meta:
        model = Contact
        fields = ('first_name', 'last_name', 'email', 'phone', 'company')

    def __init__(self, *args, **kwargs):
        self.organization = kwargs.pop('organization', None)
        self.contact = kwargs.pop('contact', None)
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['search_company'].widget.attrs['hx-post'] = reverse('search_companies', kwargs={
            'organization_uuid': self.organization.pk})

    '''
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Contact.objects.filter(user=self.request.user, email=email).exists():
            raise forms.ValidationError(_("This user and email combination already exists."))
        return email
    '''
