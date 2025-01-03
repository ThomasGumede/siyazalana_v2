import uuid, re
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

def handle_post_file_upload(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex, ext)
    return f"post/{filename}"