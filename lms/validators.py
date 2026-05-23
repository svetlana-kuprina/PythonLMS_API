from rest_framework.exceptions import ValidationError

youtube = 'youtube.com'

def validate_lesson(value):
    if youtube not in value:
       raise ValidationError ("Ссылка должна быть только на youtube.com")
    return value
