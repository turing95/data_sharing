from django.forms import ModelForm
from web_app.models import Space


class SpaceDetailForm(ModelForm):
    class Meta:
        model = Space
        fields = ['name']  # Include only the editable field
