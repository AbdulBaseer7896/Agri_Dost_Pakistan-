"""
WSGI config for agri_dost project.
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agri_dost.settings')
application = get_wsgi_application()
