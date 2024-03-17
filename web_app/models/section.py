from django.db import models
from web_app.models import BaseModel


class SpaceSection(BaseModel):
    space = models.ForeignKey('Space', on_delete=models.CASCADE, null=True, blank=True, related_name='sections')
    position = models.PositiveIntegerField(default=1)
    text_section = models.ForeignKey('TextSection', on_delete=models.CASCADE, null=True, blank=True)
    file_section = models.ForeignKey('FileSection', on_delete=models.CASCADE, null=True, blank=True)



class TextSection(BaseModel):
    space = models.ForeignKey('Space', on_delete=models.CASCADE, null=True, blank=True, related_name='text_sections')
    title = models.CharField(max_length=255)
    content = models.TextField()

    def section_form(self):
        from web_app.forms import TextSectionForm
        return TextSectionForm(instance=self, prefix=self.uuid)


class FileSection(BaseModel):
    space = models.ForeignKey('Space', on_delete=models.CASCADE, null=True, blank=True, related_name='file_sections')
    title = models.CharField(max_length=255)
    file = models.ForeignKey('File', on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField()

    def section_form(self):
        from web_app.forms import FileSectionForm
        return FileSectionForm(instance=self, prefix=self.uuid)
