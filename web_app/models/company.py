from web_app.models import BaseModel
from django.db import models
from copy import deepcopy


class Company(BaseModel):
    name = models.CharField(max_length=50)
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE, related_name='companies')
    address = models.CharField(max_length=250, null=True)
    reference_contact = models.ForeignKey('Contact', on_delete=models.SET_NULL, null=True,
                                          related_name='represented_companies')

    def __str__(self):
        return self.name

    def name_form(self, request_post=None):
        from web_app.forms import CompanyNameForm
        return CompanyNameForm(request_post, instance=self)

    def form(self, request_post=None):
        from web_app.forms import CompanyForm
        return CompanyForm(request_post, instance=self, organization=self.organization)


class CompanyTemplate(BaseModel):
    name = models.CharField(max_length=50, null=True, blank=True)
    group = models.ForeignKey('CompanyFieldGroup', on_delete=models.CASCADE, related_name='templates', null=True,
                              blank=True)
    field = models.ForeignKey('CompanyField', on_delete=models.CASCADE, related_name='templates', null=True, blank=True)
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE, related_name='company_templates')


class CompanyGroupElement(BaseModel):
    parent_group = models.ForeignKey('CompanyFieldGroup', on_delete=models.CASCADE, related_name='children_elements',
                                     null=True,
                                     blank=True)
    position = models.PositiveIntegerField(default=1)

    group = models.OneToOneField('CompanyFieldGroup', on_delete=models.CASCADE, related_name='element', null=True,
                                 blank=True)
    field = models.OneToOneField('CompanyField', on_delete=models.CASCADE, related_name='element', null=True,
                                 blank=True)

    def duplicate(self, for_template=False, parent_group=None):
        new_element = deepcopy(self)
        new_element.pk = None
        if parent_group is not None:
            new_element.parent_group = parent_group
        if self.group is not None:
            new_element.group = self.group.duplicate(for_template=for_template, group=parent_group)
        if self.field is not None:
            new_element.field = self.field.duplicate(for_template=for_template, group=parent_group)
        new_element.save()
        return new_element


class CompanyFieldGroup(BaseModel):
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE, related_name='company_field_groups', null=True)
    company = models.ForeignKey('Company', on_delete=models.CASCADE, related_name='field_groups', null=True, blank=True)
    group = models.ForeignKey('CompanyFieldGroup', on_delete=models.CASCADE, related_name='groups', null=True,
                              blank=True)
    template = models.ForeignKey('CompanyTemplate', on_delete=models.CASCADE, related_name='groups', null=True,
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
        from web_app.forms import CompanyFieldGroupSetForm
        return CompanyFieldGroupSetForm(request_post, instance=self, group=self.group)

    def duplicate(self, for_template=False, group=None):
        new_group = deepcopy(self)
        if for_template is False:
            new_group.pk = None
            if group is not None:
                new_group.group = group
                new_group.organization = group.organization
            new_group.save()
        else:
            new_group.pk = None
            new_group.group = group
            new_group.template = None
            new_group.company = None
            new_group.save()
        for element in self.children_elements.all():
            element.duplicate(for_template=for_template, parent_group=new_group)
        return new_group

    def to_template(self):
        group = self.duplicate(for_template=True)
        template = CompanyTemplate.objects.create(name=group.label if group.group else self.company.name, group=group,
                                                  organization=self.company.organization)
        self.template = template
        self.save()
        return template

    def add_template(self, template):
        group = template.group.duplicate(for_template=False, group=self)
        CompanyGroupElement.objects.create(parent_group=self, group=group, position=self.children_elements.count() + 1)


class CompanyField(BaseModel):
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE, related_name='company_fields', null=True)
    company = models.ForeignKey('Company', on_delete=models.CASCADE, related_name='fields', null=True, blank=True)
    group = models.ForeignKey('CompanyFieldGroup', on_delete=models.CASCADE, related_name='fields', null=True,
                              blank=True)
    template = models.ForeignKey('CompanyTemplate', on_delete=models.CASCADE, related_name='fields', null=True,
                                 blank=True)
    multiple = models.BooleanField(default=False)
    label = models.CharField(max_length=250)
    value = models.CharField(max_length=500, null=True, blank=True)

    def form(self, request_post=None):
        from web_app.forms import CompanyFieldFillForm
        return CompanyFieldFillForm(request_post, instance=self, prefix=self.pk)

    def set_form(self, request_post=None):
        from web_app.forms import CompanyFieldSetForm
        return CompanyFieldSetForm(request_post, instance=self, group=self.group)

    @property
    def update_event(self):
        return f'companyUpdate-{self.pk}'

    def duplicate(self, for_template=False, group=None):
        new_field = deepcopy(self)
        if for_template is False:
            new_field.pk = None
            if group is not None:
                new_field.group = group
                new_field.organization = group.organization
            new_field.save()
        else:
            new_field.pk = None
            new_field.group = group
            new_field.template = None
            new_field.company = None
            new_field.save()
        return new_field

    def to_template(self):
        company = self.company
        field = self.duplicate(for_template=True)
        template = CompanyTemplate.objects.create(name=field.label, field=field, organization=company.organization)
        self.template = template
        self.save()
        return template
