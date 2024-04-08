from django import forms



class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, multiple_files, hidden=False, *args, **kwargs):
        attrs = {}
        if hidden:
            attrs['hidden'] = True
        if multiple_files is True:

            kwargs.setdefault("widget", MultipleFileInput(attrs=attrs))
        else:
            kwargs.setdefault("widget", forms.ClearableFileInput(attrs=attrs))
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result
