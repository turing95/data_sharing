from web_app.models import BaseModel
from django.db import models


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


class CompanyField(BaseModel):
    company = models.ForeignKey('Company', on_delete=models.CASCADE, related_name='fields')
    label = models.CharField(max_length=250)
    value = models.CharField(max_length=500, null=True, blank=True)
    position = models.PositiveIntegerField(default=1)

    def form(self, request_post=None):
        from web_app.forms import CompanyFieldFillForm
        return CompanyFieldFillForm(request_post, instance=self, prefix=self.pk)

    @property
    def update_event(self):
        return f'companyUpdate-{self.pk}'
