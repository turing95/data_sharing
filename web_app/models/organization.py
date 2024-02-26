import uuid

from django.conf import settings
from django.core.mail import get_connection, EmailMultiAlternatives
from django.db import models, transaction
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.text import format_lazy
from django.utils.translation import gettext_lazy as _

from utils.emails import html_to_text
from web_app.models import BaseModel


class Organization(BaseModel):
    name = models.CharField(max_length=50)
    users = models.ManyToManyField('User', through='UserOrganization')
    created_by = models.ForeignKey('User', on_delete=models.CASCADE, related_name='created_organizations', null=True)



class UserOrganization(BaseModel):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE)
    role = models.CharField(max_length=50)


class OrganizationInvitation(BaseModel):
    email = models.EmailField()
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE)
    invited_by = models.ForeignKey('User', on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
    token = models.UUIDField(default=uuid.uuid4, editable=False)

