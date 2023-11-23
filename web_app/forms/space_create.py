from django.forms import ModelForm
from web_app.models import Space


class SpaceForm(ModelForm):
    class Meta:
        model = Space
        fields = ['name']

