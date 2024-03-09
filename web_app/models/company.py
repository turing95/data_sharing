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

    def form(self,request_post=None):
        from web_app.forms import CompanyTitleForm
        return CompanyTitleForm(request_post,instance=self)


class CompanyField(BaseModel):
    company = models.ForeignKey('Company', on_delete=models.CASCADE, related_name='fields')
    label = models.CharField(max_length=250)
    value = models.CharField(max_length=500, null=True, blank=True)

    def form(self, request_post=None):
        from web_app.forms import CompanyFieldForm
        return CompanyFieldForm(request_post, instance=self, prefix=self.pk)
