from django import forms

class ToggleSwitchWidget(forms.Widget):
    template_name =  'components/forms/toggle_widget.html'

    def __init__(self, attrs=None, color_on='green', color_off='orange', text_on='active', text_off='inactive'):
        super().__init__(attrs)
        self.color_on = color_on
        self.color_off = color_off
        self.text_on = text_on
        self.text_off = text_off

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget'].update({
            'color_on': self.color_on,
            'color_off': self.color_off,
            'text_on': self.text_on,
            'text_off': self.text_off,
        })
        return context

    def value_from_datadict(self, data, files, name):
        return data.get(name, False)