from django import forms


class ToggleWidget(forms.CheckboxInput):
    template_name = 'forms/widgets/toggle.html'

    def __init__(self, *args, **kwargs):
        # see template for supported colors, if color do not show probably they are missing in output.css, check out the template!
        self.color_on = kwargs.pop('color_on', 'blue') # color of toggle when clicked 
        self.color_off = kwargs.pop('color_off', 'gray') # color of toggle when not clicked
        self.label_on = kwargs.pop('label_on', '') # label on the right of the toggle when clicked (leave blank to not apply label)
        self.label_off = kwargs.pop('label_off', '') # label on the right of the toggle when not clicked (leave blank to not apply label)
        self.label_colored =  kwargs.pop('label_colored', False) # apply color_on and color_off to the text of the label
        self.soft_off_label = kwargs.pop('soft_off_label', False) # make label text lighter when not clicked
        self.label_wrap = kwargs.pop('label_wrap', False) # add a tag looking wrapping to the the labels, respective color is applied
        self.label_wrap_mono = kwargs.pop('label_wrap_mono', False) # if True the label wrap includes the toggle in a single visual element
        super().__init__(*args, **kwargs)
        self.attrs.update({'class': 'sr-only peer'})

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['color_on'] = self.color_on
        context['widget']['color_off'] = self.color_off
        context['widget']['label_on'] = self.label_on
        context['widget']['label_off'] = self.label_off
        context['widget']['label_on_color'] = self.color_on if self.label_colored else 'gray' # default color for labels is gray
        context['widget']['label_off_color'] = self.color_off  if self.label_colored else 'gray'
        context['widget']['soft_off_label'] = self.soft_off_label
        context['widget']['label_wrap'] = self.label_wrap
        context['widget']['label_wrap_mono'] = self.label_wrap_mono
        
        return context
