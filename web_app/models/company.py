from web_app.models import BaseModel
from django.db import models


class Company(BaseModel):
    name = models.CharField(max_length=50)
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE, related_name='companies')
    address = models.CharField(max_length=250, null=True)
    reference_contact = models.ForeignKey('Contact', on_delete=models.SET_NULL, null=True, related_name='represented_companies')

    def __str__(self):
        return self.name

    def form(self):
        from web_app.forms import CompanyUpdateForm
        return CompanyUpdateForm(instance=self)


class CompanyField(BaseModel):
    company = models.ForeignKey('Company', on_delete=models.CASCADE, related_name='fields')
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE, related_name='company_fields')
    label = models.CharField(max_length=50)
    value = models.CharField(max_length=50)
