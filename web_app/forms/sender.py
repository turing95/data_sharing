from django.forms import ModelForm
from django.urls import reverse_lazy

from web_app.forms import css_classes
from web_app.forms.widgets import SearchContactWidget, SenderToggle
from web_app.models import Sender, Contact
from django import forms
from django.utils.translation import gettext_lazy as _


class SenderCreateForm(ModelForm):
    contact = forms.ModelChoiceField(
        queryset=Contact.objects.all(),
        widget=forms.HiddenInput(),
        required=False
    )
    email = forms.EmailField(
        required=False,

        widget=SearchContactWidget(),
        help_text=_("Type the company name to search for it."))
    is_active = forms.BooleanField(
        required=False,
        widget=SenderToggle()
    )

    class Meta:
        model = Sender
        fields = ['email', 'contact', 'is_active']

    def __init__(self, *args, **kwargs):
        self.organization = kwargs.pop('organization')
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['hx-post'] = reverse_lazy('search_contacts',
                                                                    kwargs={'organization_uuid': self.organization.pk})
