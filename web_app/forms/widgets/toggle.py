from django import forms


class ToggleWidget(forms.CheckboxInput):
    template_name = 'forms/widgets/toggle.html'

    def __init__(self, *args, **kwargs):
        self.color_on = kwargs.pop('color_on', 'marian-blue')
        self.color_off = kwargs.pop('color_off', 'gray')
        self.label_on = kwargs.pop('label_on', '')
        self.label_off = kwargs.pop('label_off', '')
        self.label_colored = kwargs.pop('label_colored', False)
        self.soft_off_label = kwargs.pop('soft_off_label', False)
        self.label_wrap = kwargs.pop('label_wrap', False)
        self.label_wrap_mono = kwargs.pop('label_wrap_mono', False)
        super().__init__(*args, **kwargs)
        self.attrs.update({'class': 'sr-only peer'})

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['color_on'] = self.color_on
        context['widget']['color_off'] = self.color_off
        context['widget']['label_on'] = self.label_on
        context['widget']['label_off'] = self.label_off
        context['widget']['label_on_color'] = self.color_on if self.label_colored else 'gray'
        context['widget']['label_off_color'] = self.color_off if self.label_colored else 'gray'
        context['widget']['soft_off_label'] = self.soft_off_label
        context['widget']['label_wrap'] = self.label_wrap
        context['widget']['label_wrap_mono'] = self.label_wrap_mono

        return context
