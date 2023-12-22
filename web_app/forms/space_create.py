from django.forms import ModelForm
from web_app.models import Space
from web_app.forms import css_classes
from web_app.forms.widgets import ToggleWidget
from django import forms
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.utils import timezone as dj_timezone
from django.utils.timezone import is_aware, make_aware
from django.utils.safestring import mark_safe
from datetime import timezone
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
                            label='Space title',
                            help_text=mark_safe('''   <p class="mb-1 font-bold">Space Title</p> 
                                                        <p>It will be displayed to your invitees.</p>
                                                '''))

    is_active = forms.BooleanField(
        widget=ToggleWidget(label_on='Active',
                            label_off='Inactive'),
        required=False,
        label='Activate space',
        help_text=mark_safe('''   <p class="mb-1 font-bold">Space State at Creation</p> 
                                    <p>Set the space to 'inactive' at creation if you want to double check its properties before making it accessible to invitees.</p>
                                    <p>Set it to 'active' to make it immediately accessible to invitees and trigger the creation notifications if any.</p>
                              '''))

    senders_emails = CommaSeparatedEmailField(
        widget=forms.HiddenInput(),
        label='Senders emails',
        required=False,
        help_text=mark_safe('''   <p class="mb-1 font-bold">Invitations</p> 
                                    <p>Each invitee will have their own access link and will not be able to see any other invitee in the list.</p>
                            '''))
    email_input = forms.CharField(required=False,
                                  widget=forms.TextInput(
                                      attrs={'placeholder': 'Type or paste email addresses of invitees',
                                             'class': css_classes.text_input}))
    is_public = forms.BooleanField(
        widget=ToggleWidget(label_on='Enabled public link',
                            label_off='Disabled public link'),
        required=False,
        label='Generate public link',
        help_text=mark_safe('''   <p class="mb-1 font-bold">Public Link</p> 
                                    <p>The public link will not be tied to a specific email address and can be used to collect inputs from the general public, when there is not the need to distinguish one upload from another.</p>
                                    <p>The link can be enabled and disabled at any time, and can coexist with the invitees links.</p>
                              '''))

    instructions = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'placeholder': 'Explain what files you are requesting',
            'rows': 3,
            'class': css_classes.text_area,
        }),
        label='Instructions',
        help_text=mark_safe('''<p class="mb-1 font-bold">Instructions</p>
                                <p>These instructions will be displayed to your invitees. They refer to all the file requests in the space.</p>
                            '''))

    deadline = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local'
        }),
        help_text=mark_safe('''   <p class="mb-1 font-bold">Deadline</p> 
                                    <p>The deadline applies to all invitees and is visible in their upload page.</p>
                                    <p>You can customize what happens once the deadline is reached.</p>
                              '''))

    notify_deadline = forms.BooleanField(
        widget=ToggleWidget(label_on='Notify',
                            label_off='Notify'),
        required=False,
        label='Notify deadline',
        help_text=mark_safe('''   <p class="mb-1 font-bold">Deadline notification</p> 
                                    <p>...</p>
                              '''))

    class Meta:
        model = Space
        fields = ['title', 'is_public', 'is_active', 'instructions', 'senders_emails', 'deadline', 'notify_deadline']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.instance is not None and Space.objects.filter(pk=self.instance.pk).exists():
            space = self.instance
            self.fields['senders_emails'].initial = ','.join(
                [sender.email for sender in space.senders.filter(is_active=True)])
            self.fields['title'].disabled = True

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
            deadline = deadline.astimezone(timezone.utc)
            if deadline < arrow.utcnow():
                raise forms.ValidationError(
                    "Deadline must be in the future."
                )

        return deadline

    def save(self, commit=True):
        instance = super().save()
        instance.timezone = dj_timezone.get_current_timezone_name()
        return instance
