from django import forms

from web_app.forms import css_classes
from web_app.models import Feedback


class OutputRejectForm(forms.ModelForm):
    notes = forms.CharField(widget=forms.TextInput(attrs={'class': css_classes.text_area,
                                                          }),
                            )

    class Meta:
        fields = ['notes']
        model = Feedback
