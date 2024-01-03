from django.forms.widgets import CheckboxSelectMultiple


class CustomCheckboxSelectMultiple(CheckboxSelectMultiple):
    template_name = 'forms/widgets/restricted_files_checklist.html'
    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(name, value, label, selected, index, subindex=subindex, attrs=attrs)

        # Assuming FileType has attributes like 'uuid' and 'group'
        file_type_instance = self.choices.queryset.get(pk=value)
        option['attrs']['data-uuid'] = file_type_instance.uuid
        option['attrs']['data-group'] = 'group' if file_type_instance.group else 'single'

        return option
