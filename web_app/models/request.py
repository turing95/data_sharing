from django.db import models
from web_app.models import BaseModel


class Request(BaseModel):
    destination = models.CharField(max_length=50)  # TODO  destination model missing
    deadline = models.DateTimeField()  # TODO  deadline model missing
    space = models.ForeignKey('Space', on_delete=models.CASCADE, related_name='requests')
    number_of_files = models.IntegerField(null=True, blank=True)
