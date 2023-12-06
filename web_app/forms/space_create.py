from django.forms import ModelForm, inlineformset_factory
from web_app.models import Space, UploadRequest, FileType
from web_app.forms import css_classes
from django import forms
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from django.utils import timezone as dj_timezone
from django.utils.timezone import is_aware, make_aware, utc
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
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Untitled Space',
                                                          'class': css_classes.text_space_title_input}),
                            label='Space title')

    is_active = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={
            'class': css_classes.checkbox_input,
        }),
        required=False,
        label='Make Space active at creation'
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
        required=False
    )
    email_input = forms.CharField(required=False,
                                  widget=forms.TextInput(
                                      attrs={'placeholder': 'Type or paste email addresses of invitees',
                                             'class': css_classes.text_input}))
    deadline = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local'
        }),
    )

    class Meta:
        model = Space
        fields = ['title', 'is_public', 'is_active', 'instructions', 'senders_emails', 'deadline']
        widgets = {
            'instructions': forms.Textarea(
                attrs={'placeholder': 'Explain what files you are requesting',
                       'rows': 4,
                       'class': css_classes.text_area,
                       'label': 'Instructions'})
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_title(self):
        title = self.cleaned_data.get("title")
        user = self.user
        spaces = Space.objects.filter(user=user, title=title)
        if self.instance is not None:
            spaces = spaces.exclude(pk=self.instance.pk)
        if spaces.exists():
            raise forms.ValidationError(
                "Title already exists."
            )
        return title

    def clean_deadline(self):
        deadline = self.cleaned_data.get('deadline', None)

        if deadline is not None:
            # Ensure the datetime is timezone-aware
            if not is_aware(deadline):
                deadline = make_aware(deadline)

            # Convert to UTC
            deadline = deadline.astimezone(utc)
            if deadline < arrow.utcnow():
                raise forms.ValidationError(
                    "Deadline must be in the future."
                )

        return deadline

    def save(self, commit=True):
        instance = super().save()
        instance.timezone = dj_timezone.get_current_timezone_name()
        return instance


class FileTypeChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        # Return the string you want to display for each object
        return obj.extension


class RequestForm(ModelForm):
    FILE_NAME_INSTRUCTIONS = "Name the file as you want it to appear in your destination folder. You can use tags to make the file name parametric. Here is the list of the possible tags:"
    FILE_NAME_TAGS = "<br>" + "<br>".join([
        f"- <strong>{{{tag[1]}}}</strong> - \"{'spiegazione va qui'}\""
        for tag in UploadRequest.FileNameTag.choices
    ])

    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Untitled request',
                                                          'required': 'required',
                                                          'class': css_classes.text_request_title_input}),
                            label='Request title')

    # handling of the parametric file name
    file_naming_formula = forms.CharField(required=False,
                                          help_text=mark_safe(
                                              f"<div class='text-xs'>{FILE_NAME_INSTRUCTIONS}{FILE_NAME_TAGS}</div>"),
                                          widget=forms.TextInput(
                                              attrs={'placeholder': 'Insert file name, use tags for dynamic naming',
                                                     'class': "file-naming-formula placeholder-gray-500 my-1 min-h-[42px] min-h-32" + css_classes.text_input}),
                                          label='File naming formula')

    # Preparing the choices for the dropdown
    tag_choices = [(tag.label, tag.label) for tag in UploadRequest.FileNameTag]
    tag_choices.insert(0, ('', 'Insert parameter'))  # Add the default option

    # available tags dropdown
    available_tags_dropdown = forms.ChoiceField(
        choices=tag_choices,
        required=False,
        label='Available naming tags',
        widget=forms.Select(attrs={'class': css_classes.dropdown,
                                   'onchange': 'handleTagDropdownChange(this)'
                                   })
    )

    destination_display = forms.CharField(
        required=False,
        label='Non-editable Field',
        widget=forms.TextInput(
            attrs={'placeholder': 'Click to select a folder',
                   'class': css_classes.text_input + ' cursor-not-allowed',
                   'onclick': 'handleAuthClick(this)'})
    )

    destination = forms.CharField(
        widget=forms.HiddenInput(),
        label="Destination folder")
    token = forms.CharField(
        widget=forms.HiddenInput())

    rename = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={
            'class': css_classes.checkbox_input,
            'onclick': 'toggleRename(this);'
        }),
        required=False,
        label='Apply custom file name'
    )

    file_types = FileTypeChoiceField(
        queryset=FileType.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,  # or any other suitable widget
        label='File Types',
        help_text='Select one or more file types.'
    )

    class Meta:
        model = UploadRequest
        fields = ['title', 'file_types', 'file_naming_formula']

    def clean_file_naming_formula(self):
        file_naming_formula = self.cleaned_data.get('file_naming_formula')
        rename = self.cleaned_data.get('rename')

        if rename is False:
            file_naming_formula = '' # if checkbox is unchecked the naming formula is empty
        else:
            # List of valid tags
            valid_tags = [tag.label for tag in UploadRequest.FileNameTag]

            # Parsing the file_naming_formula for content in curly brackets
            invalid_tags = []
            start_index = file_naming_formula.find('{')
            while start_index != -1:
                end_index = file_naming_formula.find('}', start_index)
                if end_index == -1:
                    # No closing bracket found - break out of the loop
                    break

                # Extracting the tag
                tag = file_naming_formula[start_index + 1:end_index]
                if tag not in valid_tags:
                    invalid_tags.append(tag)

                # Update start_index for next iteration
                start_index = file_naming_formula.find('{', end_index)

            if invalid_tags:
                error_message = 'The following tags are not valid: ' + ', '.join(invalid_tags)
                raise forms.ValidationError(error_message)

            return file_naming_formula

    class Meta:
        model = UploadRequest
        fields = ['instructions', 'file_types', 'file_naming_formula']


RequestFormSet = inlineformset_factory(Space, UploadRequest, form=RequestForm, extra=1)
DetailRequestFormSet = inlineformset_factory(Space, UploadRequest, form=RequestForm, extra=0)
