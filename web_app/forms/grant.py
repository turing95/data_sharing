from django import forms
from django.urls import reverse_lazy

from web_app.forms import css_classes
from web_app.forms.css_classes.inputs import text_input
from django.utils.translation import gettext_lazy as _

from web_app.forms.widgets import SearchContactWidget
from web_app.models import Grant, Contact, CompanyField, CompanyFieldGroup
from django.core.exceptions import ValidationError

    # type = models.CharField(max_length=250, null=True, blank=True)
    # tags = models.TextField(null=True, blank=True) # comma separated list of tags
    # status = models.CharField(max_length=250, null=True, blank=True)

    
    
class GrantForm(forms.ModelForm):
    official_name = forms.CharField(label=_("official Name"),
                              required=False,
                              widget=forms.TextInput(attrs={'placeholder': _('Official Name'),
                                                            'class': text_input,
                                                            'hx-trigger': 'blur changed',
                                                            'hx-target': 'closest form',
                                                            'hx-swap': 'outerHTML'
                                                            }))
    official_page_link = forms.URLField(
        required=False,
        label=_('Official grant page website'),
        widget=forms.URLInput(
            attrs={'placeholder': _('Insert a website link'),
                   'class': css_classes.text_input,
                   'hx-trigger': 'blur changed',
                    'hx-target': 'closest form',
                    'hx-swap': 'outerHTML'}),
        help_text=_(""" """))
    
    application_page_link = forms.URLField(
        required=False,
        label=_('Application page link'),
        widget=forms.URLInput(
            attrs={'placeholder': _('Insert a website link'),
                   'class': css_classes.text_input,
                   'hx-trigger': 'blur changed',
                    'hx-target': 'closest form',
                    'hx-swap': 'outerHTML'}),
        help_text=_(""" """))
    
    financer_name = forms.CharField(label=_("Financer"),
                            required=False,
                            widget=forms.TextInput(attrs={'placeholder': _('Financer'),
                                                        'class': text_input,
                                                        'hx-trigger': 'blur changed',
                                                        'hx-target': 'closest form',
                                                        'hx-swap': 'outerHTML'
                                                        }))
    financer_website_link = forms.URLField(
        required=False,
        label=_('Financer Website'),
        widget=forms.URLInput(
            attrs={'placeholder': _('Insert a website link'),
                   'class': css_classes.text_input,
                   'hx-trigger': 'blur changed',
                    'hx-target': 'closest form',
                    'hx-swap': 'outerHTML'}),
        help_text=_(""" """))
    
    descriptive_timeline = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'placeholder': _('Information about the timeline'),
                                     'rows': 3,
                                     'class': css_classes.text_area,
                                     'hx-trigger': 'blur changed',
                                     'hx-target': 'closest form',
                                     'hx-swap': 'outerHTML'}),
        label=_('Timeline'),
        help_text=_(""" """))
    
    descriptive_beneficiaries = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'placeholder': _('Information about the beneficiaries'),
                                     'rows': 3,
                                     'class': css_classes.text_area,
                                     'hx-trigger': 'blur changed',
                                     'hx-target': 'closest form',
                                     'hx-swap': 'outerHTML'}),
        label=_('Beneficiaries'),
        help_text=_(""" """))

    descriptive_goals = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'placeholder': _('Information about the grant goals'),
                                     'rows': 3,
                                     'class': css_classes.text_area,
                                     'hx-trigger': 'blur changed',
                                     'hx-target': 'closest form',
                                     'hx-swap': 'outerHTML'}),
        label=_('Goals'),
        help_text=_(""" """))
    
    descriptive_funds = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'placeholder': _('Information about the available funds'),
                                     'rows': 3,
                                     'class': css_classes.text_area,
                                     'hx-trigger': 'blur changed',
                                     'hx-target': 'closest form',
                                     'hx-swap': 'outerHTML'}),
        label=_('Available funds'),
        help_text=_(""" """))

    descriptive_allowed_activities = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'placeholder': _('Information about the allowed activities'),
                                     'rows': 3,
                                     'class': css_classes.text_area,
                                     'hx-trigger': 'blur changed',
                                     'hx-target': 'closest form',
                                     'hx-swap': 'outerHTML'}),
        label=_('Allowed Activities'),
        help_text=_(""" """))
    
    descriptive_admitted_expenses = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'placeholder': _('Information about the admitted expenses'),
                                     'rows': 3,
                                     'class': css_classes.text_area,
                                     'hx-trigger': 'blur changed',
                                     'hx-target': 'closest form',
                                     'hx-swap': 'outerHTML'}),
        label=_('Amitted expenses'),
        help_text=_(""" """))  

    descriptive_not_admitted_expenses = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'placeholder': _('Information about the not admitted expenses'),
                                     'rows': 3,
                                     'class': css_classes.text_area,
                                     'hx-trigger': 'blur changed',
                                     'hx-target': 'closest form',
                                     'hx-swap': 'outerHTML'}),
        label=_('Not Admitted Expenses'),
        help_text=_(""" """))
    
    descriptive_application_iter = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'placeholder': _('Information about the Application Process'),
                                     'rows': 3,
                                     'class': css_classes.text_area,
                                     'hx-trigger': 'blur changed',
                                     'hx-target': 'closest form',
                                     'hx-swap': 'outerHTML'}),
        label=_('Application Iter'),
        help_text=_(""" """))
    
    descriptive_other = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'placeholder': _('Other information about the grant'),
                                     'rows': 3,
                                     'class': css_classes.text_area,
                                     'hx-trigger': 'blur changed',
                                     'hx-target': 'closest form',
                                     'hx-swap': 'outerHTML'}),
        label=_('Other information'),
        help_text=_(""" """))
    

    de_minimis = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': css_classes.checkbox_input,
                                          'hx-trigger': 'change',
                                          'hx-target': 'closest form',
                                          'hx-swap': 'outerHTML'}),
        label=_('De minimis'),
        help_text=_(""" """))

    class Meta:
        model = Grant
        fields = ('official_name', 'financer_name', 'financer_website_link', 'descriptive_timeline')

    def __init__(self, *args, **kwargs):
        self.organization = kwargs.pop('organization')
        super().__init__(*args, **kwargs)
        update_url = reverse_lazy('grant_update', kwargs={'grant_uuid': self.instance.pk})
        self.fields['official_name'].widget.attrs['hx-post'] = update_url
        self.fields['financer_name'].widget.attrs['hx-post'] = update_url
        self.fields['financer_website_link'].widget.attrs['hx-post'] = update_url
        self.fields['descriptive_timeline'].widget.attrs['hx-post'] = update_url

    
    # def clean(self):
    #     cleaned_data = super().clean()
    #     search_query = cleaned_data.get('email', None)
    #     if search_query:
    #         reference_contact = cleaned_data.get('reference_contact', None)
    #         if reference_contact and reference_contact.email != search_query:
    #             self.add_error('email', _('Select a contact from the list, create a new one, or leave blank.'))
    #     return cleaned_data


class GrantNameForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': _('Unnamed grant*'),
                                                         'class': css_classes.text_space_title_input,
                                                         'hx-trigger': 'blur changed',
                                                         'hx-target': 'closest form',
                                                         'hx-swap': 'outerHTML',
                                                         }),
                           label=_('Grant name'),
                           error_messages={'required': _("The name can't be empty")}
                           )

    class Meta:
        model = Grant
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance is not None:
            self.fields['name'].widget.attrs['hx-post'] = reverse_lazy('grant_update_name',
                                                                       kwargs={'grant_uuid': self.instance.pk})
