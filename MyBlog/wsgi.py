"""
WSGI config for MyBlog project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os
import sys
sys.path.append(r':/home/BOOT4')
sys.path.append(r':/home/BOOT4/MyBlog')

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MyBlog.settings')

application = get_wsgi_application()
