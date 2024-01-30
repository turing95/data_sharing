from django.db import models
from web_app.models import BaseModel


class BetaAccessRequest(BaseModel):

    user_name = models.CharField(max_length=50)
    user_email = models.CharField(max_length=50)
    industry = models.CharField(max_length=50,null=True, blank=True)
    country =  models.CharField(max_length=50,null=True, blank=True)
    company =  models.CharField(max_length=50,null=True, blank=True)
    user_role =  models.CharField(max_length=50,null=True, blank=True)
    intended_use = models.TextField(null=True, blank=True)
    first_touchpoint =  models.CharField(max_length=150,null=True, blank=True)