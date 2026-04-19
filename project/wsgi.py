"""
WSGI config for project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os
from pathlib import Path
from dotenv import load_dotenv

from django.core.wsgi import get_wsgi_application


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# DOTENV
# Por padrão, tenta carregar o arquivo .env na pasta raíz
# O override permite sobreescrever as variáveis já definidas
# Caso for para a produção, carregar os arquivos em asgi.py ou wsgi.py
load_dotenv(BASE_DIR / 'dotenv_file', override=True)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

application = get_wsgi_application()
