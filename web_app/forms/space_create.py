from django.forms import ModelForm, DateTimeInput, inlineformset_factory
from web_app.models import Space, UploadRequest
from web_app.forms.css_classes import text_input, text_area
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
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter name of the space',
                                                         'class': text_input}))
    is_active = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={
            'class': 'form-checkbox h-4 w-4 text-blue-600 transition duration-150 ease-in-out'
        }),
        required=False,
        label='Publish'
    )

    class Meta:
        model = Space
        fields = ['name', 'is_public', 'is_active', 'deadline', 'instructions']
        widgets = {
            'deadline': DateTimeInput(attrs={'type': 'datetime-local'}),
            'instructions': forms.Textarea(
                attrs={'placeholder': 'Enter instructions for the request', 'rows': 4, 'class': text_area})
        }


class RequestForm(ModelForm):
    destination = forms.CharField(
        widget=forms.TextInput(attrs={'required': 'required', 'placeholder': 'Enter destination for the request',
                                      'class': text_input}))
    number_of_files = forms.IntegerField(
        widget=forms.NumberInput(attrs={'placeholder': 'Enter number of files,leave empty for unlimited',
                                        'class': text_input}),
        required=False)
    senders_emails = CommaSeparatedEmailField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter emails separated by commas',
                                      'class': 'email-input ' + text_input}),
        label='Emails',
        required=False  # Set to True if emails are mandatory
    )

    class Meta:
        model = UploadRequest
        fields = ['number_of_files']

    def clean_emails(self):
        # Custom clean method for emails field
        emails = self.cleaned_data.get('senders_emails', [])
        return emails


RequestFormSet = inlineformset_factory(Space, UploadRequest, form=RequestForm, extra=1)
