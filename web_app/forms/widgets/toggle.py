from django import forms


class ToggleWidget(forms.CheckboxInput):
    template_name = 'forms/widgets/toggle.html'

    def __init__(self, *args, **kwargs):
                # see template for supported colors, if color do not show probably they are missing in output.css, check out the template!
        self.color_on = kwargs.pop('color_on', 'marian-blue') # color of toggle when clicked 
        self.color_off = kwargs.pop('color_off', 'gray') # color of toggle when not clicked
        self.toggle_color_on = kwargs.pop('toggle_color_on', '') # background color when on, if empty color_on is used
        self.toggle_color_off = kwargs.pop('toggle_color_off', '') # background color when off, if empty color_off is used
        self.toggle_color_off_soft = kwargs.pop('toggle_color_off_soft', True) # if true the background color when off is lighter
        self.label_on = kwargs.pop('label_on', '') # label on the right of the toggle when clicked (leave blank to not apply label)
        self.label_off = kwargs.pop('label_off', '') # label on the right of the toggle when not clicked (leave blank to not apply label)
        self.label_colored =  kwargs.pop('label_colored', False) # apply color_on and color_off to the text of the label
        self.soft_off_label = kwargs.pop('soft_off_label', True) # make label text lighter when not clicked
        self.label_wrap = kwargs.pop('label_wrap',False) # add a tag looking wrapping to the the labels, respective color is applied
        self.label_wrap_mono = kwargs.pop('label_wrap_mono', False) # if True the label wrap includes the toggle in a single visual element
        
        self.id=kwargs.pop('id','')
        super().__init__(*args, **kwargs)
        self.attrs.update({'class': 'sr-only peer'})

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['color_on'] = self.color_on
        context['widget']['color_off'] = self.color_off
        context['widget']['toggle_color_on'] = self.toggle_color_on if self.toggle_color_on else self.color_on
        context['widget']['toggle_color_off'] = self.toggle_color_off if self.toggle_color_off else self.color_off
        context['widget']['toggle_color_off_soft'] = self.toggle_color_off_soft
        context['widget']['label_on'] = self.label_on
        context['widget']['label_off'] = self.label_off
        context['widget']['label_on_color'] = self.color_on if self.label_colored else 'gray'  # default color for labels is gray
        context['widget']['label_off_color'] = self.color_off if self.label_colored else 'gray'
        context['widget']['soft_off_label'] = self.soft_off_label
        context['widget']['label_wrap'] = self.label_wrap
        context['widget']['label_wrap_mono'] = self.label_wrap_mono
        
        context['widget']['id'] = self.id

        return context
