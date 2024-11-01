from django import forms
from django.utils.translation import gettext_lazy as _
from web_app.forms import css_classes
from web_app.models import Feedback


class OutputRejectForm(forms.ModelForm):
    notes = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': _('Add a note for the sender'),
            'cols':3,
            'rows': 4,
            'class': css_classes.text_area,
        }))

    class Meta:
        fields = ['notes']
        model = Feedback
