from django.db import models
from web_app.models import BaseModel


class SpaceSection(BaseModel):
    space = models.ForeignKey('Space', on_delete=models.CASCADE, null=True, blank=True, related_name='sections')
    position = models.PositiveIntegerField(default=1)
    text_section = models.ForeignKey('TextSection', on_delete=models.CASCADE, null=True, blank=True)
    file_section = models.ForeignKey('FileSection', on_delete=models.CASCADE, null=True, blank=True)

    @classmethod
    def get_new_section_position(cls, space):
        last_position = cls.objects.filter(space=space).aggregate(models.Max('position'))['position__max']
        new_position = 1 if last_position is None else last_position + 1
        return new_position


class TextSection(BaseModel):
    title = models.CharField(max_length=255)
    content = models.TextField()

    def section_form(self):
        from web_app.forms import TextSectionForm
        return TextSectionForm(instance=self, prefix=self.uuid)


class FileSection(BaseModel):
    title = models.CharField(max_length=255)
    content = models.TextField()

    def section_form(self):
        from web_app.forms import FileSectionForm
        return FileSectionForm(instance=self, prefix=self.uuid)
