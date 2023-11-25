from django.forms import ModelForm, DateTimeInput, inlineformset_factory
from web_app.models import Space, Request
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
    senders_emails = CommaSeparatedEmailField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter emails separated by commas',
                                      'class': 'email-input bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'}),
        label='Emails',
        required=False  # Set to True if emails are mandatory
    )
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter name of the space',
                                                         'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'}))
    is_active = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={
            'class': 'form-checkbox h-4 w-4 text-blue-600 transition duration-150 ease-in-out'
        }),
        required=False,
        label='Publish'
    )

    class Meta:
        model = Space
        fields = ['name', 'is_public', 'is_active']

    def clean_emails(self):
        # Custom clean method for emails field
        emails = self.cleaned_data.get('senders_emails', [])
        return emails


class RequestForm(ModelForm):
    destination = forms.CharField(
        widget=forms.TextInput(attrs={'required': 'required', 'placeholder': 'Enter destination for the request',
                                      'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'}))
    number_of_files = forms.IntegerField(
        widget=forms.NumberInput(attrs={'placeholder': 'Enter number of files,leave empty for unlimited',
                                        'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'}),
        required=False)

    class Meta:
        model = Request
        fields = ['destination', 'deadline', 'number_of_files']
        widgets = {
            'deadline': DateTimeInput(attrs={'type': 'datetime-local'}),
        }


RequestFormSet = inlineformset_factory(Space, Request, form=RequestForm, extra=1)
