from django import forms


class ToggleWidget(forms.CheckboxInput):
    template_name = 'forms/widgets/toggle.html'

    def __init__(self, *args, **kwargs):
        self.color = kwargs.pop('color', 'blue')
        super().__init__(*args, **kwargs)
        self.attrs.update({'class': 'sr-only peer'})

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['color'] = self.color
        return context
