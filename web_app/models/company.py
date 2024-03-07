from web_app.models import BaseModel
from django.db import models


class Company(BaseModel):
    name = models.CharField(max_length=50)
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE, related_name='companies')

    def __str__(self):
        return self.name

    def form(self):
        from web_app.forms import CompanyUpdateForm
        return CompanyUpdateForm(instance=self)
