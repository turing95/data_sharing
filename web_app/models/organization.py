from django.db import models

from web_app.models import BaseModel


class Organization(BaseModel):
    name = models.CharField(max_length=50)
    users = models.ManyToManyField('User', through='UserOrganization')


class UserOrganization(BaseModel):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE)
    role = models.CharField(max_length=50)
