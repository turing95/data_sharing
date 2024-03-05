from django.forms import ModelForm
from django.urls import reverse
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


class SpaceForm(ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': _('Untitled Space*'),
                                                          'class': css_classes.text_space_title_input}),
                            label=_('Space title - MANDATORY'),
                            help_text=_("It will be displayed to your invitees"))
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

    senders_emails = CommaSeparatedEmailField(
        widget=forms.HiddenInput(),
        label=_('Senders emails'),
        required=False,
        help_text=_(
            "Each invitee will have their own access link and will not be able to see any other invitee in the list."))

    email_input = forms.CharField(required=False,
                                  widget=forms.TextInput(
                                      attrs={'placeholder': _('Type or paste email addresses of invitees'),
                                             'class': css_classes.text_input + "email-input"}))
    notify_invitation = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class': css_classes.checkbox_input}),
        required=False,
        label=_('Invitation notification'),
        help_text=_(
            """All invitees will receive an email with the link to the space upon creation. You can re-send the invitation at any time."""))
    is_public = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class': css_classes.checkbox_input}),
        required=False,
        label=_('Public link'),
        help_text=_("""The public link will not be tied to a specific email address and can be used to collect inputs from the general public, when there is not the need to distinguish one upload from another.
                            The link can be enabled and disabled at any time, and can coexist with the invitees links.
                            """))

    instructions = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'placeholder': _('Explain what files you are requesting'),
            'rows': 3,
            'class': css_classes.text_area,
        }),
        label=_('Instructions'),
        help_text=_("""These instructions will be displayed to your invitees. They refer to all the file requests in the space.
                            """))

    deadline = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': css_classes.datetime_input
        }, format='%Y-%m-%dT%H:%M:%S'),
        help_text=_("""The deadline applies to all invitees and is visible in their upload page.
                                You can customize what happens once the deadline is reached.
                                """))
    deadline_notice_days = forms.IntegerField(
        required=False,
        min_value=0,
        max_value=15,
        localize=True,
        widget=forms.NumberInput(attrs={
            'placeholder': _('Days'),
            'step': '1',  # Set step for increments
            'value': '1',  # Default value
            'class': css_classes.inline_text_input
        }),
        label=_('Days before deadline'),
        help_text=_('Number of days before the deadline to send notifications.')
    )

    deadline_notice_hours = forms.IntegerField(
        required=False,
        localize=True,
        min_value=0,
        max_value=23,
        widget=forms.NumberInput(attrs={
            'placeholder': _('Hours'),
            'step': '1',  # Set step for increments
            'value': '0',  # Default value
            'class': css_classes.inline_text_input
        }),
        label=_('Hours before deadline'),
        help_text=_('Number of hours before the deadline to send notifications.')
    )

    upload_after_deadline = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class': css_classes.checkbox_input}),
        required=False,
        label=_('Uploads after deadline'),
        help_text=_("""Your invitees will be able to upload files after the deadline if this is enabled.
        You can change this setting at any time."""))

    notify_deadline = forms.BooleanField(
        widget=ToggleWidget(label_on=_('Notification'),
                            label_off=_('Notification')),
        required=False,
        label=_('Notify deadline'),
        help_text=_("""Set a number of days and hours before the deadline to send a notification to your invitees."""))

    class Meta:
        model = Space
        fields = ['title', 'is_public', 'instructions', 'senders_emails', 'deadline', 'notify_deadline',
                  'notify_invitation', 'company',
                  'upload_after_deadline', 'deadline_notice_days', 'deadline_notice_hours']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.organization = kwargs.pop('organization', None)
        super().__init__(*args, **kwargs)
        self.fields['search_company'].widget.attrs['hx-post'] = reverse('search_companies', kwargs={
            'organization_uuid': self.organization.pk})
        if self.instance is not None and Space.objects.filter(pk=self.instance.pk).exists():
            space = self.instance
            if space.company:
                self.fields['search_company'].initial = space.company.name
            self.fields['senders_emails'].initial = ','.join(
                [sender.email for sender in space.senders.filter(is_active=True)])

    def clean_deadline(self):
        deadline = self.cleaned_data.get('deadline', None)

        if deadline is not None:
            '''# Ensure the datetime is timezone-aware
            if not is_aware(deadline):
                deadline = make_aware(deadline)'''
            # Convert to UTC
            deadline = arrow.get(deadline).to('UTC')
            if deadline < arrow.utcnow():
                if self.instance is None or self.instance.deadline != deadline:
                    raise forms.ValidationError(
                        _("Deadline must be in the future.")
                    )

            return deadline.isoformat()
        return deadline

    def clean(self):
        cleaned_data = super().clean()

        # Assuming you have a field for deadline in your form
        deadline = cleaned_data.get('deadline')
        notify_deadline = cleaned_data.get('notify_deadline')
        deadline_notice_days = cleaned_data.get('deadline_notice_days')
        deadline_notice_hours = cleaned_data.get('deadline_notice_hours')

        if not deadline or not notify_deadline:
            cleaned_data['deadline_notice_days'] = None
            cleaned_data['deadline_notice_hours'] = None
        else:
            # Calculate notification datetime in the server timezone
            notification_dt = arrow.get(deadline).shift(days=-deadline_notice_days, hours=-deadline_notice_hours)

            # Get the current time in the server timezone
            current_dt = arrow.now()

            # Check if current time is past the notification time
            if current_dt > notification_dt:
                error_message = _("Current time is past the deadline notification time.")
                self.add_error('deadline_notice_days', error_message)
                self.add_error('deadline_notice_hours', error_message)

        return cleaned_data

    def save(self, commit=True):
        instance = super().save()
        instance.timezone = dj_timezone.get_current_timezone_name()
        instance.locale = translation.get_language()
        return instance


class SpaceUpdateForm(ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': _('Untitled Space*'),
                                                          'class': css_classes.text_space_title_input}),
                            label=_('Space title - MANDATORY'),
                            help_text=_("It will be displayed to your invitees"))
    instructions = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'placeholder': _('Explain what files you are requesting'),
            'rows': 3,
            'class': css_classes.text_area,
        }),
        label=_('Instructions'),
        help_text=_("""These instructions will be displayed to your invitees. They refer to all the file requests in the space.
                            """))

    class Meta:
        model = Space
        fields = ['title', 'instructions']
