from django.forms import ModelForm
from web_app.models import Space
from django import forms
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


class CommaSeparatedEmailField(forms.CharField):

    def to_python(self, value):
        if not value:
            return []
        return [email.strip() for email in value.split(',')]

    def validate(self, value):
        super().validate(value)
        for email in value:
            try:
                validate_email(email)
            except ValidationError:
                raise ValidationError(f"{email} is not a valid email address")


class SpaceForm(ModelForm):
    emails = CommaSeparatedEmailField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter emails separated by commas', 'class': 'email-input'}),
        label='Emails',
        required=False  # Set to True if emails are mandatory
    )

    class Meta:
        model = Space
        fields = ['name']

    def clean_emails(self):
        # Custom clean method for emails field
        emails = self.cleaned_data.get('emails', [])
        return emails
