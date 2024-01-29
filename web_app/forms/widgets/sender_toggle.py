from web_app.forms.widgets import ToggleWidget


class SenderToggle(ToggleWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(color_on="green",
                         color_off="orange",
                         toggle_color_on="marian-blue",
                         toggle_color_off="gray",
                         label_on="active",
                         label_off="inactive",
                         soft_off_label=False,
                         label_colored=True,
                         label_wrap=True)
        self.attrs.update({'class': 'sr-only peer sender-push'})
