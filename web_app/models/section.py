from django.db import models
from web_app.models import BaseModel

 
class SpaceSection(BaseModel):
    space = models.ForeignKey('Space', on_delete=models.CASCADE, null=True, blank=True, related_name='sections')
    position = models.PositiveIntegerField(default=1)
    heading_section = models.ForeignKey('HeadingSection', on_delete=models.CASCADE, null=True, blank=True)
    paragraph_section = models.ForeignKey('ParagraphSection', on_delete=models.CASCADE, null=True, blank=True)
    file_section = models.ForeignKey('FileSection', on_delete=models.CASCADE, null=True, blank=True)



class HeadingSection(BaseModel):
    space = models.ForeignKey('Space', on_delete=models.CASCADE, null=True, blank=True, related_name='heading_sections')
    title = models.CharField(max_length=255)

    def section_form(self):
        from web_app.forms import HeadingSectionForm
        return HeadingSectionForm(instance=self, prefix=self.uuid)

class ParagraphSection(BaseModel):
    space = models.ForeignKey('Space', on_delete=models.CASCADE, null=True, blank=True, related_name='paragraph_sections')
    content = models.TextField()

    def section_form(self):
        from web_app.forms import ParagraphSectionForm
        return ParagraphSectionForm(instance=self, prefix=self.uuid)


class FileSection(BaseModel):
    space = models.ForeignKey('Space', on_delete=models.CASCADE, null=True, blank=True, related_name='file_sections')
    title = models.CharField(max_length=255)
    file = models.ForeignKey('File', on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField()

    def section_form(self):
        from web_app.forms import FileSectionForm
        return FileSectionForm(instance=self, prefix=self.uuid)
