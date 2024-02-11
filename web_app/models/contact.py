from web_app.models import BaseModel, ActiveModel
from django.db import models


class Contact(BaseModel, ActiveModel):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    company = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(max_length=50)
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='contacts')

    class Meta:
        unique_together = ['email', 'user']
