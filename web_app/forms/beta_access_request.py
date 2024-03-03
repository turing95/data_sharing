from django.forms import ModelForm
from web_app.models import BetaAccessRequest
from web_app.forms import css_classes
from django import forms
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class BetaAccessRequestForm(ModelForm):
    user_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': _('John Doe'),
                                                              'class': css_classes.text_input}),
                                label=_('User Name'),
                                help_text=_(""))

    user_email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': _('jhon.doe@mail.com'),
                                                               'class': css_classes.text_input}),
                                 label=_('User Email'),
                                 help_text=_("This email will be used to grant you access to the beta version, pay attention to the spelling or you will not hear from us."))
    
    industry = forms.CharField(widget=forms.TextInput(attrs={'placeholder': _('Finance'),
                                                             'class': css_classes.text_input}),
                               required=False,
                               label=_('Industry'),
                               help_text=_(""))

    country = forms.CharField(widget=forms.TextInput(attrs={'placeholder': _('United States'),
                                                            'class': css_classes.text_input}),
                              required=False,
                              label=_('Country'),
                              help_text=_(""))

    company = forms.CharField(widget=forms.TextInput(attrs={'placeholder': _('Acme Inc.'),
                                                            'class': css_classes.text_input}),
                              required=False,
                              label=_('Company'),
                              help_text=_(""))

    user_role = forms.CharField(widget=forms.TextInput(attrs={'placeholder': _('Accountant'),
                                                              'class': css_classes.text_input}),
                                required=False,
                                label=_('Role'),
                                help_text=_(""))

    intended_use = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': _('Explain what you would like to use Kezyy for'),
            'rows': 3,
            'class': css_classes.text_area,
        }),
        label=_('Intended use'),
        help_text=_(""" """))

    first_touchpoint = forms.CharField(widget=forms.TextInput(attrs={'placeholder': _('Linkedin'),
                                                                     'class': css_classes.text_input}),
                                       required=False,
                                       label=_('First Touchpoint'),
                                       help_text=_(""))
    honeypot = forms.CharField(required=False,
                               widget=forms.TextInput(attrs={'class': 'hidden'}))

    class Meta:
        model = BetaAccessRequest
        fields = ['user_name', 'user_email', 'industry', 'country', 'company', 'user_role', 'intended_use',
                  'first_touchpoint']

    def clean_user_email(self):
        email = self.cleaned_data.get('user_email', None)
        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError(_(f"{email} is not a valid email address"))
        return email

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('honeypot', None):
            raise ValidationError(_("You are a robot"))
        return cleaned_data