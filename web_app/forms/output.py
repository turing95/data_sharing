from django import forms

from web_app.forms import css_classes


class OutputRejectForm(forms.Form):
    notes = forms.CharField(widget=forms.TextInput(attrs={'class': css_classes.text_area,
                                                          }),
                            )
