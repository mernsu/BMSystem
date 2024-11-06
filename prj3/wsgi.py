"""
WSGI config for prj3 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os,sys

from django.core.wsgi import get_wsgi_application

virtualenv_dir = r'C:\ProgramData\anaconda3\envs\prj3\Lib\site-packages'
sys.path.insert(0, virtualenv_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "prj3.settings")
os.environ["DJANGO_SETTINGS_MODULE"] = "{{ project_name }}.settings"
application = get_wsgi_application()
