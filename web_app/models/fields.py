from web_app.models import BaseModel
from django.db import models
from copy import deepcopy
from docxtpl import DocxTemplate


class FieldTemplate(BaseModel):
    name = models.CharField(max_length=250, null=True, blank=True)
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE, related_name='field_group_templates')
    group = models.OneToOneField('FieldGroup', on_delete=models.CASCADE, related_name='derived_template',
                                 null=True)
    text_field = models.OneToOneField('TextField', on_delete=models.CASCADE, related_name='derived_template', null=True)
    file_field = models.OneToOneField('FileField', on_delete=models.CASCADE, related_name='derived_template', null=True)


class GroupElement(BaseModel):
    parent_group = models.ForeignKey('FieldGroup', on_delete=models.CASCADE, related_name='children_elements',
                                     null=True,
                                     blank=True)
    position = models.PositiveIntegerField(default=1)
    group = models.OneToOneField('FieldGroup', on_delete=models.CASCADE, related_name='element', null=True,
                                 blank=True)
    text_field = models.OneToOneField('TextField', on_delete=models.CASCADE, related_name='element', null=True,
                                      blank=True)
    file_field = models.OneToOneField('FileField', on_delete=models.CASCADE, related_name='element', null=True,
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
        if self.file_field is not None:
            new_element.file_field = self.file_field.duplicate(for_template=for_template, group=parent_group)
        new_element.save()
        return new_element


class FieldGroup(BaseModel):
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE, related_name='field_groups',
                                     null=True)
    company = models.ForeignKey('Company', on_delete=models.CASCADE, related_name='field_groups', null=True, blank=True)
    grant = models.ForeignKey('Grant', on_delete=models.CASCADE, related_name='field_groups', null=True, blank=True)
    group = models.ForeignKey('FieldGroup', on_delete=models.CASCADE, related_name='groups', null=True,
                              blank=True)
    template = models.ForeignKey('FieldTemplate', on_delete=models.CASCADE, related_name='groups', null=True,
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

    def duplicate(self, for_template=False, group=None, grant=None):
        new_group = deepcopy(self)
        new_group.pk = None
        if group is not None:
            new_group.group = group
            new_group.organization = group.organization
            new_group.company = group.company
            new_group.grant = grant or group.grant
        if for_template is True:
            new_group.template = None
            new_group.company = None
            new_group.grant = None
        new_group.save()
        for element in self.children_elements.all():
            element.duplicate(for_template=for_template, parent_group=new_group)
        return new_group

    def to_template(self):
        group = self.duplicate(for_template=True)
        organization = self.company.organization if self.company is not None else self.grant.organization

        template = FieldTemplate.objects.create(
            name=group.label if group.group else (self.company.name if self.company else self.grant.name),
            group=group,
            organization=organization)
        self.template = template
        self.save()
        return template

    def add_template(self, template):
        if template.group:
            group = template.group.duplicate(for_template=False, group=self)
            GroupElement.objects.create(parent_group=self, group=group, position=self.children_elements.count() + 1)
        elif template.text_field:
            text_field = template.text_field.duplicate(for_template=False, group=self)
            GroupElement.objects.create(parent_group=self, text_field=text_field,
                                        position=self.children_elements.count() + 1)
        elif template.file_field:
            file_field = template.file_field.duplicate(for_template=False, group=self)
            GroupElement.objects.create(parent_group=self, file_field=file_field,
                                        position=self.children_elements.count() + 1)

    def to_request(self, space, label=None):
        from web_app.models import Request, InputRequest, TextRequest, UploadRequest
        request = Request.objects.create(space=space, title=label or self.label)
        position = 1
        for element in self.children_elements.all():
            if element.group:
                child_request = element.group.to_request(space)
                InputRequest.objects.create(request=request, child_request=child_request, position=position)
                position += 1
            elif element.text_field and element.text_field.fill_from is False:
                TextRequest.objects.filter(target=element.text_field).update(target=None)
                text_request = TextRequest.objects.create(request=request, target=element.text_field,
                                                          title=element.text_field.label)
                InputRequest.objects.create(request=request, text_request=text_request, position=position)
                position += 1
            elif element.file_field and element.text_field.fill_from is False:
                UploadRequest.objects.filter(target=element.file_field).update(target=None)
                upload_request = UploadRequest.objects.create(request=request, target=element.file_field,
                                                              title=element.file_field.label)
                InputRequest.objects.create(request=request, upload_request=upload_request, position=position)
                position += 1
        return request


class TextField(BaseModel):
    group = models.ForeignKey('FieldGroup', on_delete=models.CASCADE, related_name='text_fields', null=True,
                              blank=True)
    template = models.ForeignKey('FieldTemplate', on_delete=models.CASCADE, related_name='text_fields', null=True)
    multiple = models.BooleanField(default=False)
    label = models.CharField(max_length=250)
    value = models.CharField(max_length=500, null=True, blank=True)
    fill_from = models.ForeignKey('TextField', on_delete=models.SET_NULL, related_name='filling_fields', null=True)

    @property
    def update_event(self):
        return f'fieldUpdate-{self.pk}'

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

    def fill(self, value=None):
        if value is not None:
            self.value = value
            self.save()
        for field in self.filling_fields.all():
            field.fill(self.value)

    def to_template(self):
        text_field = self.duplicate(for_template=True)
        organization = self.group.organization
        template = FieldTemplate.objects.create(
            name=text_field.label,
            text_field=text_field,
            organization=organization)
        self.template = template
        self.save()
        return template


class FileField(BaseModel):
    group = models.ForeignKey('FieldGroup', on_delete=models.CASCADE, related_name='file_fields', null=True,
                              blank=True)
    template = models.ForeignKey('FieldTemplate', on_delete=models.CASCADE, related_name='file_fields', null=True)
    multiple = models.BooleanField(default=False)
    label = models.CharField(max_length=250)
    multiple_files = models.BooleanField(default=False)
    fill_from = models.ForeignKey('FileField', on_delete=models.SET_NULL, related_name='filling_fields', null=True)

    def form(self, request_post=None, files=None):
        from web_app.forms import FileFieldFillForm
        return FileFieldFillForm(request_post, files, instance=self, prefix=self.pk)

    def set_form(self, request_post=None):
        from web_app.forms import FileFieldSetForm
        return FileFieldSetForm(request_post, instance=self, group=self.group)

    def duplicate(self, for_template=False, group=None):
        new_field = deepcopy(self)
        new_field.pk = None
        if group is not None:
            new_field.group = group
        if for_template is True:
            new_field.template = None
        new_field.save()
        return new_field

    def fill(self, file=None):
        from web_app.models import FileFileField
        if file is not None:
            FileFileField.objects.get_or_create(field=self, file=file)
        for field in self.filling_fields.all():
            field.fill(file)

    def to_template(self):
        file_field = self.duplicate(for_template=True)
        organization = self.group.organization
        template = FieldTemplate.objects.create(
            name=file_field.label,
            file_field=file_field,
            organization=organization)
        self.template = template
        self.save()
        return template


class FileFileField(BaseModel):
    field = models.ForeignKey('FileField', on_delete=models.CASCADE, related_name='files')
    file = models.OneToOneField('File', on_delete=models.CASCADE, related_name='file_field', null=True, blank=True)
    template = models.OneToOneField('File', on_delete=models.CASCADE, related_name='file_field_template', null=True, )

    class Meta:
        ordering = ['-created_at']

    def get_filled_template(self):
        # return FileResponse(open(path_to_file, 'rb'), as_attachment=True, filename="my_filename")
        with open(self.file.file, 'rb') as f:
            try:
                doc = DocxTemplate(f)
            except Exception as e:
                return None
            company = self.field.group.company
            grant = self.field.group.grant
            context = {'company': company, 'grant': grant}
            doc.render(context)
            doc.save("filled_template.docx")
            return doc.docx
