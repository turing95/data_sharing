from django.core.management.base import BaseCommand
from web_app.models import FileType

class Command(BaseCommand):
    help = 'Populates the database with common file extensions and descriptive slugs'

    def handle(self, *args, **kwargs):
        # List of common file extensions with descriptive slugs
        common_extensions = [
            {'group': False, 'slug': 'PDF', 'extension': 'pdf'},
            {'group': False, 'slug': 'Word Doc', 'extension': 'doc'},
            {'group': False, 'slug': 'Word DocX', 'extension': 'docx'},
            {'group': False, 'slug': 'PowerPoint', 'extension': 'ppt'},
            {'group': False, 'slug': 'PowerPointX', 'extension': 'pptx'},
            {'group': False, 'slug': 'Excel Sheet', 'extension': 'xls'},
            {'group': False, 'slug': 'Excel SheetX', 'extension': 'xlsx'},
            {'group': False, 'slug': 'Text File', 'extension': 'txt'},
            {'group': False, 'slug': 'JPEG Image (jpg)', 'extension': 'jpg'},
            {'group': False, 'slug': 'JPEG Image (jpeg)', 'extension': 'jpeg'},
            {'group': False, 'slug': 'PNG Image', 'extension': 'png'},
            {'group': False, 'slug': 'GIF Image', 'extension': 'gif'},
            {'group': False, 'slug': 'BMP Image', 'extension': 'bmp'},
            {'group': False, 'slug': 'TIFF Image', 'extension': 'tiff'},
            {'group': False, 'slug': 'SVG Image', 'extension': 'svg'},
            {'group': False, 'slug': 'MP3 Audio', 'extension': 'mp3'},
            {'group': False, 'slug': 'WAV Audio', 'extension': 'wav'},
            {'group': False, 'slug': 'AAC Audio', 'extension': 'aac'},
            {'group': False, 'slug': 'OGG Audio', 'extension': 'ogg'},
            {'group': False, 'slug': 'FLAC Audio', 'extension': 'flac'},
            {'group': False, 'slug': 'MP4 Video', 'extension': 'mp4'},
            {'group': False, 'slug': 'MOV Video', 'extension': 'mov'},
            {'group': False, 'slug': 'WMV Video', 'extension': 'wmv'},
            {'group': False, 'slug': 'FLV Video', 'extension': 'flv'},
            {'group': False, 'slug': 'AVI Video', 'extension': 'avi'},
            {'group': False, 'slug': 'MKV Video', 'extension': 'mkv'},
            {'group': False, 'slug': 'Zip Archive', 'extension': 'zip'},
            {'group': False, 'slug': 'RAR Archive', 'extension': 'rar'},
            {'group': False, 'slug': '7z Archive', 'extension': '7z'},
            {'group': False, 'slug': 'GZ Archive', 'extension': 'gz'},
            {'group': False, 'slug': 'TAR Archive', 'extension': 'tar'},
            {'group': False, 'slug': 'JSON Data', 'extension': 'json'},
            {'group': False, 'slug': 'XML Data', 'extension': 'xml'},
            {'group': False, 'slug': 'CSV Data', 'extension': 'csv'},
            {'group': False, 'slug': 'HTML File', 'extension': 'html'},
            {'group': False, 'slug': 'CSS Style', 'extension': 'css'},
            {'group': False, 'slug': 'JavaScript File', 'extension': 'js'},
            {'group': False, 'slug': 'PHP Script', 'extension': 'php'},
            {'group': False, 'slug': 'Python Script', 'extension': 'py'},
            {'group': False, 'slug': 'Java File', 'extension': 'java'},
        ]

        for ext in common_extensions:
            FileType.objects.get_or_create(
                slug=ext['slug'],
                defaults={
                    'group': ext['group'],
                    'extension': ext['extension']
                }
            )

        self.stdout.write(self.style.SUCCESS('Successfully populated file types with descriptive slugs'))
