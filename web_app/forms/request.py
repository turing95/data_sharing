import re
from django.forms import BaseInlineFormSet, inlineformset_factory, ModelForm
from django.core.exceptions import ValidationError
from web_app.models import Space, UploadRequest, FileType, GoogleDrive, OneDrive, SharePoint, Kezyy
from web_app.forms import css_classes
from django.urls import reverse_lazy
from django import forms

from django.utils.safestring import mark_safe
from web_app.forms.widgets import ToggleWidget
from django.utils.translation import gettext_lazy as _


class CommaSeparatedFileTypeField(forms.CharField):

    def to_python(self, value):
        if not value:
            return []
        file_types = []
        for slug in value.split(','):
            file_type = FileType.objects.filter(slug=slug).first()
            if file_type is None:
                raise ValidationError(_("{slug} is not a valid file type"))
            file_types.append(file_type)
        return file_types


class RequestForm(ModelForm):
    instance: UploadRequest
    FILE_NAME_INSTRUCTIONS = _("Name the file as you want it to appear in your destination folder. You can use tags to make the file name parametric. Here is the list of the possible tags:")
    FILE_NAME_TAGS = "<br>" + "<br>".join([
        f"- <strong>{{{tag[1]}}}</strong>"
        for tag in UploadRequest.FileNameTag.choices
    ])

    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': _('Untitled request*'),
                                                          'required': 'required',
                                                          'class': css_classes.text_request_title_input}),
                            label=_('Request title - MANDATORY'),
                            help_text=_("""This will be displayed to your invitees. Assign a meaningful title to your request to help your invitees understand what you are asking for."""))

    # handling of the parametric file name
    file_naming_formula = forms.CharField(required=False,
                                          help_text=mark_safe(
                                              f"<div class='text-xs'>{FILE_NAME_INSTRUCTIONS}{FILE_NAME_TAGS}</div>"),
                                          widget=forms.TextInput(
                                              attrs={'placeholder': _('Insert file name, use tags for dynamic naming'),
                                                     'class': "file-naming-formula placeholder-gray-500 my-1 min-h-[42px] min-h-32" + css_classes.text_input}),
                                          label=_('File naming formula'))

    # Preparing the choices for the dropdown
    tag_choices = [(tag.label, tag.label) for tag in UploadRequest.FileNameTag]
    tag_choices.insert(0, ('', _('Insert parameter')))  # Add the default option

    # available tags dropdown
    available_tags_dropdown = forms.ChoiceField(
        choices=tag_choices,
        required=False,
        label=_('Available naming tags'),
        widget=forms.Select(attrs={'class': css_classes.dropdown,
                                   'onchange': 'handleTagDropdownChange(this)'
                                   })
    )

    destination_type_select = forms.ChoiceField(
        choices=[
            (GoogleDrive.TAG, 'Google Drive'),
            (OneDrive.TAG, 'OneDrive'),
            (SharePoint.TAG, 'SharePoint'),
            (Kezyy.TAG, 'Kezyy'),
        ],
        label="Destination folder",
        widget=forms.Select(
            attrs={
                'class': "bg-gray-50 border border-gray-300 text-gray-900 text-sm flex-grow w-full h-full select-destination-type",
                'hx-trigger': "change, load, intersect once",
                'hx-get': reverse_lazy('select_destination_type'),
                'hx-target': "previous .destination-search",
                'hx-swap': "outerHTML",
                })
    )

    destination_id = forms.CharField(
        required=False,
        widget=forms.HiddenInput(attrs={'class': 'destination'}),
        label=_("Destination folder ID"),
        help_text=_("""The file uploaded for this request will be sent to the folder selected here. Choose a cloud storage provider and search for a folder and select it."""))
    sharepoint_site_id = forms.CharField(
        required=False,
        widget=forms.HiddenInput(attrs={'class': 'sharepoint-site'}))
    destination_type = forms.CharField(widget=forms.HiddenInput(attrs={
        'class': 'destination-type',
        'hx-trigger': "change, load, intersect once",
        'hx-post': reverse_lazy('get_destination_logo'),
        'hx-target': "previous .destination-logo",
        'hx-swap': "outerHTML",
        'hx-include': 'this'
    }),
        label=_("Destination type")

    )

    destination_display = forms.CharField(
        required=False,
        label=_('Non-editable Field'),
        widget=forms.TextInput(
            attrs={
                'class': ' w-full h-full px-2 py-1 text-base truncate focus:ring-0 focus:outline-none focus:border-0 bg-transparent border-none sm:text-sm' + ' destination-display',
                'readonly': 'readonly',
                'placeholder': _('No folder selected yet')
            }
        )
    )

    # REQUEST INSTRUCTIONS
    instructions = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'placeholder': _('Add request-specific instructions here'),
            'rows': 2,
            'class': css_classes.text_area,
        }),
        label=_('Request Instructions'),
        help_text=_("""Use this to provide additional information for your invitees that are specific to the request.
                                Leave blank if not necessary.
                            """))

    rename = forms.BooleanField(
        widget=ToggleWidget(label_on=_('Custom file names'),
                            label_off=_('Custom file names'),
                            attrs={
                                'onclick': 'toggleRename(this)'
                            }),
        required=False,
        label=_('File Naming'),
        help_text=_("""By default, files are saved to your destination folder with the name they have been uploaded with.
                You can choose to apply a custom file name to add parametric information to the file names to make them more meaningful and standardized
            """))
    multiple_files = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class': css_classes.checkbox_input}),
        required=False,
        label=_('Multiple Files'),
        help_text=_("""
                By default, each request can only contain one file. You can choose to enable multiple files upload for this request.
            """))
    file_template = forms.URLField(
        required=False,
        label=_('File Template'),
        widget=forms.URLInput(
            attrs={'placeholder': _('Insert file template URL'),
                   'class': css_classes.text_input}),
        help_text=_("""
                You can provide a template file that will be available for download to your invitees. 
                Leave blank if not necessary.
            """))

    class Meta:
        model = UploadRequest
        fields = ['title', 'file_naming_formula', 'instructions', 'multiple_files', 'file_template']

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        index = kwargs.pop('index', 0)
        super().__init__(*args, **kwargs)
        self.fields['destination_type_select'].widget.attrs[
            'hx-get'] += f'?next={request.get_full_path()}&request_index={index}'
        self.fields['destination_type'].widget.attrs[
            'hx-post'] += f'?request_index={index}'
        if not request.user.sharepoint_sites:
            self.fields['destination_type_select'].choices = [
                (GoogleDrive.TAG, 'Google Drive'),
                (OneDrive.TAG, 'OneDrive'),
                (Kezyy.TAG, 'Kezyy'),
            ]
        if self.instance and UploadRequest.objects.filter(pk=self.instance.pk).exists():
            destination = self.instance.destination
            if self.instance.file_naming_formula is not None:
                self.fields['rename'].initial = True
            if destination:
                self.fields['destination_id'].initial = destination.folder_id
                self.fields['destination_display'].initial = destination.name
                self.fields['destination_type'].initial = destination.tag
                self.fields['destination_type_select'].initial = destination.tag


    def clean_file_naming_formula(self):
        file_naming_formula = self.cleaned_data.get('file_naming_formula')
        valid_tags = [tag.label for tag in UploadRequest.FileNameTag]

        # Regular expression to find content within curly brackets
        regex_pattern = r"\{{([^}]+)\}}"
        found_tags = re.findall(regex_pattern, file_naming_formula)

        # Filtering out invalid tags
        invalid_tags = [tag for tag in found_tags if tag not in valid_tags]

        if invalid_tags:
            error_message = 'The following tags are not valid: ' + ', '.join(invalid_tags)
            self.add_error('file_naming_formula', error_message)

        return file_naming_formula

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('destination_id') is None:
            if cleaned_data.get('destination_type') != Kezyy.TAG:
                self.add_error('destination_id', 'You must select a folder!')
        rename = cleaned_data.get('rename', False)
        file_naming_formula = cleaned_data.get('file_naming_formula', None)
        if rename is False:
            cleaned_data['file_naming_formula'] = None
        else:
            if file_naming_formula is None or file_naming_formula == '':
                # self.add_error('file_naming_formula', 'You must provide a file name if you want to rename the files.')
                cleaned_data['file_naming_formula'] = None
        return cleaned_data


class DetailRequestForm(RequestForm):
    uuid = forms.UUIDField(
        widget=forms.HiddenInput(),
    )

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.fields['uuid'].initial = self.instance.uuid


class CustomInlineFormSet(BaseInlineFormSet):

    def get_form_kwargs(self, index):
        kwargs = super().get_form_kwargs(index)
        kwargs["index"] = index
        return kwargs


RequestFormSet = inlineformset_factory(Space, UploadRequest, form=RequestForm, formset=CustomInlineFormSet, extra=1)
DetailRequestFormSet = inlineformset_factory(Space, UploadRequest, form=DetailRequestForm, formset=CustomInlineFormSet,
                                             extra=0)
