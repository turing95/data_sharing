import re
from django.forms import BaseInlineFormSet, inlineformset_factory, ModelForm
from web_app.models import Request, UploadRequest, GoogleDrive, OneDrive, SharePoint, Kezyy, TextRequest
from web_app.forms import css_classes
from django.urls import reverse_lazy
from django import forms

from django.utils.safestring import mark_safe
from web_app.forms.widgets import ToggleWidget
from django.utils.translation import gettext_lazy as _


class UploadRequestForm(ModelForm):
    instance: UploadRequest
    FILE_NAME_INSTRUCTIONS = _(
        "Name the file as you want it to appear in your destination folder. You can use tags to make the file name parametric. Here is the list of the possible tags:")
    FILE_NAME_TAGS = "<br>" + "<br>".join([
        f"- <strong>{{{tag[1]}}}</strong>"
        for tag in UploadRequest.FileNameTag.choices
    ])
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': _('Untitled request'),
                                                          'class': css_classes.text_request_title_input,
                                                          'hx-trigger': 'blur changed'}),
                            required=False,
                            label=_('Request title - MANDATORY'),
                            help_text=_(
                                """This will be displayed to your invitees. Assign a meaningful title to your request to help your invitees understand what you are asking for."""))

    # handling of the parametric file name
    file_naming_formula = forms.CharField(required=False,
                                          help_text=mark_safe(
                                              f"<div class='text-xs'>{FILE_NAME_INSTRUCTIONS}{FILE_NAME_TAGS}</div>"),
                                          widget=forms.TextInput(
                                              attrs={'placeholder': _('Insert file name, use tags for dynamic naming'),
                                                     'hx-trigger': 'blur changed',
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
        required=False,
        label="Destination folder",
        widget=forms.Select(
            attrs={
                'class': "bg-gray-50 border border-gray-300 text-gray-900 text-sm flex-grow w-full h-full select-destination-type",
                'hx-trigger': "change, load, intersect once",
                'hx-target': "previous .destination-search",
                'hx-swap': "outerHTML",
            })
    )

    destination_id = forms.CharField(
        required=False,
        widget=forms.HiddenInput(attrs={'class': 'destination'}),
        label=_("Destination folder ID"),
        help_text=_(
            """The file uploaded for this request will be sent to the folder selected here. Choose a cloud storage provider and search for a folder and select it."""))
    sharepoint_site_id = forms.CharField(
        required=False,
        widget=forms.HiddenInput(attrs={'class': 'sharepoint-site', 'hx-trigger': 'change'}))
    destination_type = forms.CharField(widget=forms.HiddenInput(attrs={
        'class': 'destination-type',
        'hx-trigger': "change, load, intersect once",
        'hx-target': "previous .destination-logo",
        'hx-swap': "outerHTML",
        'hx-include': 'this'
    }),
        label=_("Destination type"),
        required=False

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
                   'class': css_classes.text_input,
                   'hx-trigger': 'blur changed'}),
        help_text=_("""
                You can provide a template file that will be available for download to your invitees. 
                Leave blank if not necessary.
            """))

    class Meta:
        model = UploadRequest
        fields = ['title', 'file_naming_formula', 'multiple_files', 'file_template']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        update_url = reverse_lazy('upload_request_update', kwargs={'upload_request_uuid': self.instance.pk})
        self.fields['destination_id'].widget.attrs['hx-post'] = update_url
        self.fields['title'].widget.attrs['hx-post'] = update_url
        self.fields['file_naming_formula'].widget.attrs['hx-post'] = update_url
        self.fields['file_template'].widget.attrs['hx-post'] = update_url
        self.fields['multiple_files'].widget.attrs['hx-post'] = update_url
        self.fields['rename'].widget.attrs['hx-post'] = update_url
        self.fields['destination_type'].widget.attrs[
            'hx-post'] = reverse_lazy('get_destination_logo', kwargs={'upload_request_uuid': self.instance.pk})
        self.fields['destination_type'].widget.attrs[
            'hx-post'] = reverse_lazy('get_destination_logo', kwargs={'upload_request_uuid': self.instance.pk})
        self.fields['destination_type_select'].widget.attrs[
            'hx-get'] = reverse_lazy('select_destination_type', kwargs={'upload_request_uuid': self.instance.pk})
        '''self.fields['destination_type_select'].widget.attrs[
            'hx-get'] += f'?next={request.get_full_path()}'''
        if not user.sharepoint_sites:
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


class TextRequestForm(ModelForm):
    title = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': _('Untitled request'),
                                                                          'class': css_classes.text_request_title_input}))

    class Meta:
        model = TextRequest
        fields = ['title']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        update_url = reverse_lazy('text_request_update', kwargs={'text_request_uuid': self.instance.pk})
        self.fields['title'].widget.attrs['hx-post'] = update_url


class RequestForm(ModelForm):
    instance: Request

    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': _('Untitled request'),
                                                          'required': 'required',
                                                          'class': css_classes.text_space_title_input,
                                                          'hx-trigger': 'blur changed',
                                                          'hx-target': 'closest .request-form',
                                                          'hx-swap': 'outerHTML'
                                                          }),
                            label=_('Title - MANDATORY'),
                            help_text=_(
                                """This will be displayed to your invitees. Assign a meaningful title to your request to help your invitees understand what you are asking for."""))

    instructions = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'placeholder': _('Add instructions here'),
            'rows': 3,
            'class': css_classes.text_area,
            'hx-trigger': 'blur changed',
            'hx-target': 'closest .request-form',
            'hx-swap': 'outerHTML'
        }),
        label=_('Instructions'),
        help_text=_("""Use this to provide information for your invitees.
                                Leave blank if not necessary.
                            """))

    class Meta:
        model = Request
        fields = ['title', 'instructions']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        update_url = reverse_lazy('request_detail', kwargs={'request_uuid': self.instance.pk})
        self.fields['title'].widget.attrs['hx-post'] = update_url
        self.fields['instructions'].widget.attrs['hx-post'] = update_url
