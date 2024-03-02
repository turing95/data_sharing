from django.forms import ModelForm
from web_app.models import Space
from web_app.forms import css_classes
from web_app.forms.widgets import ToggleWidget
from django import forms
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.utils import timezone as dj_timezone
from django.utils import translation
import arrow


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
                raise ValidationError(f"{invalid_emails[0]} is not a valid email address")
            else:
                raise ValidationError(f"{', '.join(invalid_emails)} are not valid email addresses")


class SpaceForm(ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Untitled Space*',
                                                          'class': css_classes.text_space_title_input}),
                            label='Space title - MANDATORY',
                            help_text="It will be displayed to your invitees")
    company = forms.ModelChoiceField(
        queryset=None,
        required=True,
        label='Company',
        help_text="Select the company to which the space belongs.")

    senders_emails = CommaSeparatedEmailField(
        widget=forms.HiddenInput(),
        label='Senders emails',
        required=False,
        help_text="Each invitee will have their own access link and will not be able to see any other invitee in the list.")

    email_input = forms.CharField(required=False,
                                  widget=forms.TextInput(
                                      attrs={'placeholder': 'Type or paste email addresses of invitees',
                                             'class': css_classes.text_input + "email-input"}))
    notify_invitation = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class': css_classes.checkbox_input}),
        required=False,
        label='Invitation notification',
        help_text="""All invitees will receive an email with the link to the space upon creation. You can re-send the invitation at any time.""")
    is_public = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class': css_classes.checkbox_input}),
        required=False,
        label='Public link',
        help_text="""The public link will not be tied to a specific email address and can be used to collect inputs from the general public, when there is not the need to distinguish one upload from another.
                            The link can be enabled and disabled at any time, and can coexist with the invitees links.
                            """)

    instructions = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'placeholder': 'Explain what files you are requesting',
            'rows': 3,
            'class': css_classes.text_area,
        }),
        label='Instructions',
        help_text="""These instructions will be displayed to your invitees. They refer to all the file requests in the space.
                            """)

    deadline = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': css_classes.datetime_input
        }, format='%Y-%m-%dT%H:%M:%S'),
        help_text="""The deadline applies to all invitees and is visible in their upload page.
                                You can customize what happens once the deadline is reached.
                                """)
    deadline_notice_days = forms.IntegerField(
        required=False,
        min_value=0,
        max_value=15,
        localize=True,
        widget=forms.NumberInput(attrs={
            'placeholder': 'Days',
            'step': '1',  # Set step for increments
            'value': '1',  # Default value
            'class': css_classes.inline_text_input
        }),
        label='Days before deadline',
        help_text='Number of days before the deadline to send notifications.'
    )

    deadline_notice_hours = forms.IntegerField(
        required=False,
        localize=True,
        min_value=0,
        max_value=23,
        widget=forms.NumberInput(attrs={
            'placeholder': 'Hours',
            'step': '1',  # Set step for increments
            'value': '0',  # Default value
            'class': css_classes.inline_text_input
        }),
        label='Hours before deadline',
        help_text='Number of hours before the deadline to send notifications.'
    )

    upload_after_deadline = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class': css_classes.checkbox_input}),
        required=False,
        label='Uploads after deadline',
        help_text="""Your invitees will be able to upload files after the deadline if this is enabled.
        You can change this setting at any time.""")

    notify_deadline = forms.BooleanField(
        widget=ToggleWidget(label_on='Notification',
                            label_off='Notification'),
        required=False,
        label='Notify deadline',
        help_text="""Set a number of days and hours before the deadline to send a notification to your invitees.""")

    class Meta:
        model = Space
        fields = ['title', 'is_public', 'instructions', 'senders_emails', 'deadline', 'notify_deadline',
                  'notify_invitation','company',
                  'upload_after_deadline', 'deadline_notice_days', 'deadline_notice_hours']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.organization = kwargs.pop('organization', None)
        super().__init__(*args, **kwargs)
        self.fields['company'].queryset = self.organization.companies.all()
        if self.instance is not None and Space.objects.filter(pk=self.instance.pk).exists():
            space = self.instance
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
                        "Deadline must be in the future."
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
                error_message = "Current time is past the deadline notification time."
                self.add_error('deadline_notice_days', error_message)
                self.add_error('deadline_notice_hours', error_message)

        return cleaned_data

    def save(self, commit=True):
        instance = super().save()
        instance.timezone = dj_timezone.get_current_timezone_name()
        instance.locale = translation.get_language()
        return instance
