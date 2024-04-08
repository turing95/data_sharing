from django.forms import ModelForm
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from web_app.models import Space, Company
from web_app.forms import css_classes
from web_app.forms.widgets import ToggleWidget
from django import forms
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.utils import timezone as dj_timezone
from django.utils import translation
import arrow


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


class CommaSeparatedEmailField(forms.CharField):

    def to_python(self, value):
        if not value:
            return []
        return [email.strip() for email in value.split(',')]

    def validate(self, value):
        super().validate(value)
        invalid_emails = []
        for email in value:
            try:
                validate_email(email)
            except ValidationError:
                invalid_emails.append(email)
        if invalid_emails:
            if len(invalid_emails) == 1:
                raise ValidationError(_(f"{invalid_emails[0]} is not a valid email address"))
            else:
                raise ValidationError(_(f"{', '.join(invalid_emails)} are not valid email addresses"))


class SpaceSettingsForm(ModelForm):
    company = CompanyField(
        widget=forms.HiddenInput(),
        required=False,
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
    notify_invitation = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class': css_classes.checkbox_input}),
        required=False,
        label=_('Invitation notification'),
        help_text=_(
            """All invitees will receive an email with the link to the space upon creation. You can re-send the invitation at any time."""))
    source_grant = forms.ModelChoiceField(
        queryset=None,
        required=False,
        label=_('Grant'),
        help_text=_("Select the grant that originated this space."))


    class Meta:
        model = Space
        fields = ['company','source_grant']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.organization = kwargs.pop('organization', None)
        super().__init__(*args, **kwargs)
        self.fields['search_company'].widget.attrs['hx-post'] = reverse('search_companies', kwargs={
            'organization_uuid': self.organization.pk})
        self.fields['source_grant'].queryset = self.organization.grants.filter(space__isnull=True)
        if self.instance is not None and Space.objects.filter(pk=self.instance.pk).exists():
            if self.instance.company:
                self.fields['search_company'].initial = self.instance.company.name



    def save(self, commit=True):
        instance = super().save()
        instance.timezone = dj_timezone.get_current_timezone_name()
        instance.locale = translation.get_language()
        return instance


class SpaceTitleForm(ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': _('Untitled Space*'),
                                                          'class': css_classes.text_space_title_input,
                                                          'hx-trigger': 'blur changed',
                                                          'hx-target': 'closest form',
                                                          'hx-swap': 'outerHTML'
                                                          }),
                            label=_('Space title - MANDATORY'),
                            help_text=_("It will be displayed to your invitees"))

    class Meta:
        model = Space
        fields = ['title']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance is not None and Space.objects.filter(pk=self.instance.pk).exists():
            self.fields['title'].widget.attrs['hx-post'] = reverse_lazy('space_update',
                                                                        kwargs={'space_uuid': self.instance.pk})
  
