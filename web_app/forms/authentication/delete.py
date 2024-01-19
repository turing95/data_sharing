from django import forms


class DeleteForm(forms.Form):
    username = forms.BooleanField()
