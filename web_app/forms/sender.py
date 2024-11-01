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
        help_text=_("Type the company name to search for it."))
 

    class Meta:
        model = Sender
        fields = ['email', 'contact']

    def __init__(self, *args, **kwargs):
        self.organization = kwargs.pop('organization')
        super().__init__(*args, **kwargs)
        sender = kwargs['instance']
        url = reverse_lazy('search_contacts', kwargs={'organization_uuid': self.organization.pk})
        query_param = '?sender_uuid=' + str(sender.pk)
        full_url = str(url) + query_param        
        self.fields['email'].widget=SearchContactWidget(sender_uuid=sender.pk)
        self.fields['email'].widget.attrs['hx-post'] = full_url
        


class SenderNotifyForm(forms.Form):
    subject = forms.CharField(widget=forms.TextInput(attrs={'class': css_classes.text_input,
                                                            }), required=False
                              )
    content = forms.CharField(widget=forms.TextInput(attrs={'class': css_classes.text_area,
                                                            }), required=False
                              )
