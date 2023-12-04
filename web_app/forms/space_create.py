from django.forms import ModelForm, inlineformset_factory
from web_app.models import Space, UploadRequest
from web_app.forms.css_classes import text_input, text_area, text_space_title_input
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
                                                         'class': text_space_title_input}),
                            label='Space title')
    
    is_active = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={
            'class': 'form-checkbox h-4 w-4 text-blue-600 transition duration-150 ease-in-out'
        }),
        required=False,
        label='Publish'
    )
    senders_emails = CommaSeparatedEmailField(
        widget=forms.HiddenInput(),
        label='Senders emails',
        required=False  # Set to True if emails are mandatory
    )
    email_input = forms.CharField(required=False,
                                  widget=forms.TextInput(attrs={'placeholder': 'Type or paste email addresses of invitees','class':text_input}))

    class Meta:
        model = Space
        fields = ['title', 'is_public', 'is_active', 'instructions', 'senders_emails']
        widgets = {
            'instructions': forms.Textarea(
                attrs={'placeholder': 'Explain what files you are requesting',
                       'rows': 4,
                       'class': text_area,
                       'label': 'Instructions'})
        }


class RequestForm(ModelForm):
    destination = forms.CharField(
        widget=forms.TextInput(attrs={'required': 'required', 'placeholder': 'Enter destination for the request',
                                      'class': text_input}))
    token = forms.CharField(
        widget=forms.HiddenInput())
    rename = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={
            'class': 'form-checkbox h-4 w-4 text-blue-600 transition duration-150 ease-in-out',
            'onclick': 'renameToggle(this);'
        }),
        required=False,
        label='Rename files'
    )
    file_name = forms.CharField(required=False,
        widget=forms.TextInput(attrs={'placeholder': 'File name',
                                      'class': text_input}))

    class Meta:
        model = UploadRequest
        fields = ['instructions', 'file_type', 'file_name']


RequestFormSet = inlineformset_factory(Space, UploadRequest, form=RequestForm, extra=1)
