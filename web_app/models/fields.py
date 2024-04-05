from web_app.models import BaseModel
from django.db import models
from copy import deepcopy


class FieldGroupTemplate(BaseModel):
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE, related_name='field_group_templates')
    group = models.OneToOneField('FieldGroup', on_delete=models.CASCADE, related_name='derived_template',
                                 null=True)


class GroupElement(BaseModel):
    parent_group = models.ForeignKey('FieldGroup', on_delete=models.CASCADE, related_name='children_elements',
                                     null=True,
                                     blank=True)
    position = models.PositiveIntegerField(default=1)
    group = models.OneToOneField('FieldGroup', on_delete=models.CASCADE, related_name='element', null=True,
                                 blank=True)
    text_field = models.OneToOneField('TextField', on_delete=models.CASCADE, related_name='element', null=True,
                                      blank=True)

    def duplicate(self, for_template=False, parent_group=None):
        new_element = deepcopy(self)
        new_element.pk = None
        if parent_group is not None:
            new_element.parent_group = parent_group
        if self.group is not None:
            new_element.group = self.group.duplicate(for_template=for_template, group=parent_group)
        if self.text_field is not None:
            new_element.text_field = self.text_field.duplicate(for_template=for_template, group=parent_group)
        new_element.save()
        return new_element


class FieldGroup(BaseModel):
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE, related_name='field_groups',
                                     null=True)
    company = models.ForeignKey('Company', on_delete=models.CASCADE, related_name='field_groups', null=True, blank=True)
    group = models.ForeignKey('FieldGroup', on_delete=models.CASCADE, related_name='groups', null=True,
                              blank=True)
    template = models.OneToOneField('FieldGroupTemplate', on_delete=models.CASCADE, related_name='groups', null=True,
                                    blank=True)
    multiple = models.BooleanField(default=False)
    label = models.CharField(max_length=250, null=True, blank=True)

    @property
    def update_event(self):
        return f'groupUpdate-{self.pk}'

    @property
    def ordered_elements(self):
        return self.children_elements.all().order_by('position')

    def set_form(self, request_post=None):
        from web_app.forms import FieldGroupSetForm
        return FieldGroupSetForm(request_post, instance=self, group=self.group)

    def duplicate(self, for_template=False, group=None):
        new_group = deepcopy(self)
        new_group.pk = None
        if group is not None:
            new_group.group = group
            new_group.organization = group.organization
            new_group.company = group.company
        if for_template is True:
            new_group.template = None
            new_group.company = None
        new_group.save()
        for element in self.children_elements.all():
            element.duplicate(for_template=for_template, parent_group=new_group)
        return new_group

    def to_template(self):
        group = self.duplicate(for_template=True)
        template = FieldGroupTemplate.objects.create(name=group.label if group.group else self.company.name, group=group,
                                                  organization=self.company.organization)
        self.template = template
        self.save()
        return template

    def add_template(self, template):
        group = template.group.duplicate(for_template=False, group=self)
        GroupElement.objects.create(parent_group=self, group=group, position=self.children_elements.count() + 1)


class TextField(BaseModel):
    group = models.ForeignKey('FieldGroup', on_delete=models.CASCADE, related_name='fields', null=True,
                              blank=True)
    multiple = models.BooleanField(default=False)
    label = models.CharField(max_length=250)
    value = models.CharField(max_length=500, null=True, blank=True)

    def form(self, request_post=None):
        from web_app.forms import TextFieldFillForm
        return TextFieldFillForm(request_post, instance=self, prefix=self.pk)

    def set_form(self, request_post=None):
        from web_app.forms import TextFieldSetForm
        return TextFieldSetForm(request_post, instance=self, group=self.group)

    def duplicate(self, for_template=False, group=None):
        new_field = deepcopy(self)
        new_field.pk = None
        if group is not None:
            new_field.group = group
        if for_template is True:
            new_field.template = None
        new_field.save()
        return new_field
