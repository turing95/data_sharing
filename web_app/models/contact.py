from web_app.models import BaseModel, ActiveModel
from django.db import models


class Contact(BaseModel, ActiveModel):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50,unique=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='contacts')
