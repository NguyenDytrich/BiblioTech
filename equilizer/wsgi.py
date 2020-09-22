***REMOVED***
WSGI config for equilizer project.

It exposes the WSGI callable as a module-level variable named ``application``.

***REMOVED***
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
***REMOVED***

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'equilizer.settings')

application = get_wsgi_application()
