from django.core.management.base import BaseCommand
from web_app.models import FileType
from django.utils.translation import gettext_lazy as _

class Command(BaseCommand):
    help = _('Populates the database with common file extensions and descriptive slugs')

    def handle(self, *args, **kwargs):
        # List of common file extensions with descriptive slugs
        common_extensions = [
    {"group": False, "slug": "PDF - pdf", "extension": "pdf"},
    {"group": False, "slug": "Word Doc - doc", "extension": "doc"},
    {"group": False, "slug": "Word DocX - docx", "extension": "docx"},
    {"group": False, "slug": "PowerPoint - ppt", "extension": "ppt"},
    {"group": False, "slug": "PowerPointX - pptx", "extension": "pptx"},
    {"group": False, "slug": "Excel Sheet - xls", "extension": "xls"},
    {"group": False, "slug": "Excel SheetX - xlsx", "extension": "xlsx"},
    {"group": False, "slug": "Text File - txt", "extension": "txt"},
    {"group": False, "slug": "JPEG Image (jpg) - jpg", "extension": "jpg"},
    {"group": False, "slug": "JPEG Image (jpeg) - jpeg", "extension": "jpeg"},
    {"group": False, "slug": "PNG Image - png", "extension": "png"},
    {"group": False, "slug": "GIF Image - gif", "extension": "gif"},
    {"group": False, "slug": "BMP Image - bmp", "extension": "bmp"},
    {"group": False, "slug": "TIFF Image - tiff", "extension": "tiff"},
    {"group": False, "slug": "SVG Image - svg", "extension": "svg"},
    {"group": False, "slug": "MP3 Audio - mp3", "extension": "mp3"},
    {"group": False, "slug": "WAV Audio - wav", "extension": "wav"},
    {"group": False, "slug": "AAC Audio - aac", "extension": "aac"},
    {"group": False, "slug": "OGG Audio - ogg", "extension": "ogg"},
    {"group": False, "slug": "FLAC Audio - flac", "extension": "flac"},
    {"group": False, "slug": "MP4 Video - mp4", "extension": "mp4"},
    {"group": False, "slug": "MOV Video - mov", "extension": "mov"},
    {"group": False, "slug": "WMV Video - wmv", "extension": "wmv"},
    {"group": False, "slug": "FLV Video - flv", "extension": "flv"},
    {"group": False, "slug": "AVI Video - avi", "extension": "avi"},
    {"group": False, "slug": "MKV Video - mkv", "extension": "mkv"},
    {"group": False, "slug": "Zip Archive - zip", "extension": "zip"},
    {"group": False, "slug": "RAR Archive - rar", "extension": "rar"},
    {"group": False, "slug": "7z Archive - 7z", "extension": "7z"},
    {"group": False, "slug": "GZ Archive - gz", "extension": "gz"},
    {"group": False, "slug": "TAR Archive - tar", "extension": "tar"},
    {"group": False, "slug": "JSON Data - json", "extension": "json"},
    {"group": False, "slug": "XML Data - xml", "extension": "xml"},
    {"group": False, "slug": "CSV Data - csv", "extension": "csv"},
    {"group": False, "slug": "HTML File - html", "extension": "html"},
    {"group": False, "slug": "CSS Style - css", "extension": "css"},
    {"group": False, "slug": "JavaScript File - js", "extension": "js"},
    {"group": False, "slug": "PHP Script - php", "extension": "php"},
    {"group": False, "slug": "Python Script - py", "extension": "py"},
    {"group": False, "slug": "Java File - java", "extension": "java"}
        ]

        for ext in common_extensions:
            FileType.objects.get_or_create(
                slug=ext['slug'],
                defaults={
                    'group': ext['group'],
                    'extension': ext['extension']
                }
            )

        self.stdout.write(self.style.SUCCESS(_('Successfully populated file types with descriptive slugs')))
