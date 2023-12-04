from django.forms import ModelForm, inlineformset_factory
from web_app.models import Space, UploadRequest, FileType
from web_app.forms import css_classes
from django import forms
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe


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
                            label='Space title')

    is_active = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={
            'class': css_classes.checkbox_input,
        }),
        required=False,
        label='Publish'
    )
    is_public = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={
            'class': css_classes.checkbox_input,
        }),
        required=False,
        label='Generate public link'
    )
    senders_emails = CommaSeparatedEmailField(
        widget=forms.HiddenInput(),
        label='Senders emails',
        required=False  # Set to True if emails are mandatory
    )
    email_input = forms.CharField(required=False,
                                  widget=forms.TextInput(
                                      attrs={'placeholder': 'Type or paste email addresses of invitees',
                                             'class': css_classes.text_input}))

    class Meta:
        model = Space
        fields = ['title', 'is_public', 'is_active', 'instructions', 'senders_emails']
        widgets = {
            'instructions': forms.Textarea(
                attrs={'placeholder': 'Explain what files you are requesting',
                       'rows': 4,
                       'class': css_classes.text_area,
                       'label': 'Instructions'})
        }


class FileTypeChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        # Return the string you want to display for each object
        return obj.extension


class RequestForm(ModelForm):

    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Untitled request',
                                                          'required': 'required',
                                                          'class': 'bg-transparent w-1/2 text-gray-900 p-1 border-t-0 border-x-0 border-b border-b-gray-400 transition-all duration-300 text-sm    hover:border-black #hover:text-sm    focus:outline-none focus:ring-0 font-bold'}),
                            label='Request title')

    file_name_instructions = "Name the file as you want it to appear in your destination folder. You can use tags to make the file name parametric. Here is the list of the possible tags:"
    file_name_tags = "<br>" + "<br>".join([
        f"- <strong>{{{tag[1]}}}</strong> - \"{'spiegazione va qui'}\""
        for tag in UploadRequest.FileNameTag.choices
    ])
    file_name = forms.CharField(required=False,
                                help_text=mark_safe(
                                    f"<div class='text-xs'>{file_name_instructions}{file_name_tags}</div>"),
                                widget=forms.TextInput(
                                    attrs={'placeholder': 'Insert file name, use tags for dynamic naming',
                                           'class': css_classes.text_input}),
                                initial='{original file name}',
                                label='File naming')

    destination = forms.CharField(
        widget=forms.TextInput(attrs={'required': 'required',
                                      'placeholder': 'Enter destination for the request',
                                      'class': css_classes.text_input}))
    token = forms.CharField(
        widget=forms.HiddenInput())

    rename = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={
            'class': css_classes.checkbox_input,
            'onclick': 'renameToggle(this);'
        }),
        required=False,
        label='Rename files'
    )
    file_types = FileTypeChoiceField(
        queryset=FileType.objects.all(),
        required=True,
        widget=forms.CheckboxSelectMultiple,  # or any other suitable widget
        label='File Types',
        help_text='Select one or more file types.'
    )

    class Meta:
        model = UploadRequest
        fields = ['instructions', 'file_types', 'file_name']


RequestFormSet = inlineformset_factory(Space, UploadRequest, form=RequestForm, extra=1)
