from django.forms import ModelForm
from web_app.models import Space
from web_app.forms import css_classes
from web_app.forms.widgets import ToggleWidget
from django import forms
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.utils import timezone as dj_timezone
from django.utils.timezone import is_aware, make_aware
from datetime import timezone
import arrow
from decimal import Decimal


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
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Untitled Space',
                                                          'class': css_classes.text_space_title_input}),
                            label='Space title',
                            help_text="It will be displayed to your invitees")

    is_active = forms.BooleanField(
        widget=ToggleWidget(label_on='Active',
                            label_off='Inactive'),
        required=False,
        label='Activate space',
        help_text="""Set the space to 'inactive' at creation if you want to double check its properties before making it accessible to invitees.
                            Set it to 'active' to make it immediately accessible to invitees and trigger the creation notifications if any.
                             """)

    senders_emails = CommaSeparatedEmailField(
        widget=forms.HiddenInput(),
        label='Senders emails',
        required=False,
        help_text="Each invitee will have their own access link and will not be able to see any other invitee in the list.")
    
    email_input = forms.CharField(required=False,
                                  widget=forms.TextInput(
                                      attrs={'placeholder': 'Type or paste email addresses of invitees',
                                             'class': css_classes.text_input + "email-input"}))
    is_public = forms.BooleanField(
        widget=ToggleWidget(label_on='Enabled public link',
                            label_off='Disabled public link'),
        required=False,
        label='Generate public link',
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
            'type': 'datetime-local'
        }),
        help_text="""The deadline applies to all invitees and is visible in their upload page.
                                You can customize what happens once the deadline is reached.
                                """)
    deadline_notice_days = forms.DecimalField(
        required=False,
        min_value=Decimal('0'),
        max_value=Decimal('15'),
        decimal_places=1,
        max_digits=3,
        widget=forms.NumberInput(attrs={
            'placeholder': 'Days', 
            'step': '1',  # Set step for increments
            'value': '1',  # Default value
            'class': css_classes.inline_num_input
        }),
        label='Days before deadline',
        help_text='Number of days before the deadline to send notifications.'
    )

    deadline_notice_hours = forms.DecimalField(
        required=False,
        min_value=Decimal('0'),
        max_value=Decimal('23.9'),
        decimal_places=1,
        max_digits=4,
        widget=forms.NumberInput(attrs={
            'placeholder': 'Hours', 
            'step': '0.5',  # Set step for increments
            'value': '0',  # Default value
            'class': css_classes.inline_num_input
        }),
        label='Hours before deadline',
        help_text='Number of hours before the deadline to send notifications.'
    )
    
    upload_after_deadline = forms.BooleanField(
        widget=ToggleWidget(label_on='Uploads after deadline allowed',
                            label_off='Uploads after deadline not allowed'),
        required=False,
        label='Allow uploads after deadline',
        help_text="""Your invitees will not be able to upload files after the deadline if this is enabled.
        You can change this setting at any time.""")
    
    notify_deadline = forms.BooleanField(
        widget=ToggleWidget(label_on='Notify',
                            label_off='Notify'),
        required=False,
        label='Notify deadline',
        help_text="""...""")

    class Meta:
        model = Space
        fields = ['title', 'is_public', 'is_active', 'instructions', 'senders_emails', 'deadline', 'notify_deadline', 'upload_after_deadline', 'deadline_notice_days', 'deadline_notice_hours']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.instance is not None and Space.objects.filter(pk=self.instance.pk).exists():
            space = self.instance
            self.fields['senders_emails'].initial = ','.join(
                [sender.email for sender in space.senders.filter(is_active=True)])
            self.fields['title'].disabled = True

    def clean_deadline(self):
        deadline = self.cleaned_data.get('deadline', None)

        if deadline is not None:
            # Ensure the datetime is timezone-aware
            if not is_aware(deadline):
                deadline = make_aware(deadline)
            # Convert to UTC
            deadline = arrow.get(deadline).to('UTC')
            if deadline < arrow.utcnow():
                if self.instance is None or self.instance.deadline != deadline:
                    raise forms.ValidationError(
                        "Deadline must be in the future."
                    )

            return deadline.isoformat()
        return deadline
    
    def clean_instructions(self):
        instructions = self.cleaned_data.get('instructions', None)
        if instructions is not None:
            return instructions
        return instructions
    
    def clean(self):
        cleaned_data = super().clean()

        # Assuming you have a field for deadline in your form
        deadline = cleaned_data.get('deadline')
        deadline_notice_days = cleaned_data.get('deadline_notice_days')
        deadline_notice_hours = cleaned_data.get('deadline_notice_hours')

        if not deadline:
            cleaned_data['deadline_notice_days'] = None
            cleaned_data['deadline_notice_hours'] = None
        else:
            # Convert Decimal values to float
            notice_days = float(deadline_notice_days) if deadline_notice_days is not None else 0
            notice_hours = float(deadline_notice_hours) if deadline_notice_hours is not None else 0

            # Calculate notification datetime in the server timezone
            notification_dt = arrow.get(deadline).shift(days=-notice_days, hours=-notice_hours)

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
        return instance
