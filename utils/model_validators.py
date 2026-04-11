from django.core.exceptions import ValidationError


def validate_png(image):
    # Verifica se a extensão da imagem é .png
    if not image.name.lower().endswith('.png'):
        raise ValidationError('Imagem precisa ser PNG')
