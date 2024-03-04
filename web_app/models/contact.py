from web_app.models import BaseModel, ActiveModel
from django.db import models


class Contact(BaseModel, ActiveModel):
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    company = models.ForeignKey('Company', on_delete=models.CASCADE, related_name='contacts', null=True)
    email = models.EmailField(max_length=50)
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='contacts')
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE, related_name='contacts', null=True)

    @property
    def full_name(self):
        if not self.first_name and not self.last_name:
            return None
        return f"{self.first_name or ''} {self.last_name or ''}"
