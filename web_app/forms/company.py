from django import forms
from django.urls import reverse_lazy

from web_app.forms import css_classes
from web_app.forms.css_classes.inputs import text_input
from django.utils.translation import gettext_lazy as _

from web_app.forms.widgets import SearchContactWidget
from web_app.models import Company, Contact, CompanyField


class CompanyForm(forms.ModelForm):
    address = forms.CharField(label=_("Address"),
                              required=False,
                              widget=forms.TextInput(attrs={'placeholder': _('Address'),
                                                            'class': text_input,
                                                            'hx-trigger': 'blur changed',
                                                            'hx-target': 'closest form',
                                                            'hx-swap': 'outerHTML'
                                                            }))
    reference_contact = forms.ModelChoiceField(
        queryset=Contact.objects.all(),
        widget=forms.HiddenInput(attrs={'hx-trigger': 'change',
                                        'hx-target': 'closest form',
                                        'hx-swap': 'outerHTML'}),
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
            if self.instance.reference_contact:
                self.fields['email'].initial = self.instance.reference_contact.email
            self.fields['address'].widget.attrs['hx-post'] = reverse_lazy('company_update',
                                                                          kwargs={'company_uuid': self.instance.pk})
            self.fields['reference_contact'].widget.attrs['hx-post'] = reverse_lazy('company_update',
                                                                                    kwargs={
                                                                                        'company_uuid': self.instance.pk})


class CompanyNameForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': _('Unnamed company*'),
                                                         'class': css_classes.text_space_title_input,
                                                         'hx-trigger': 'blur changed',
                                                         'hx-target': 'closest form',
                                                         'hx-swap': 'outerHTML',
                                                         }),
                           label=_('Company name'),
                           error_messages={'required': _("The name can't be empty.")}
                           )

    class Meta:
        model = Company
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance is not None:
            self.fields['name'].widget.attrs['hx-post'] = reverse_lazy('company_update_name',
                                                                       kwargs={'company_uuid': self.instance.pk})


class CompanyFieldForm(forms.ModelForm):
    label = forms.CharField(widget=forms.TextInput(attrs={'class': css_classes.text_input,
                                                          'hx-trigger': 'blur changed',
                                                          'hx-target': 'closest form',
                                                          'hx-swap': 'outerHTML'
                                                          }),
                            )
    value = forms.CharField(widget=forms.TextInput(attrs={'class': css_classes.text_input,
                                                          'hx-trigger': 'blur changed',
                                                          'hx-target': 'closest form',
                                                          'hx-swap': 'outerHTML'

                                                          }),
                            )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance is not None:
            self.fields['value'].widget.attrs['hx-post'] = reverse_lazy('company_field_update',
                                                                        kwargs={'company_field_uuid': self.instance.pk})
            self.fields['label'].widget.attrs['hx-post'] = reverse_lazy('company_field_update',
                                                                        kwargs={'company_field_uuid': self.instance.pk})

    class Meta:
        model = CompanyField
        fields = ['value', 'label']
