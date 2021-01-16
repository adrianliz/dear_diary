from django.core.wsgi import get_wsgi_application
import os
import sys
sys.path.append('/home/alumno/django/dear_diary')
sys.path.append(
    '/home/alumno/miniconda3/envs/djangoEnv/lib/python3.8/site-packages')

os.environ['DJANGO_SETTINGS_MODULE'] = 'dear_diary.settings'

application = get_wsgi_application()
