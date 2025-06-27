# -*- coding: utf-8 -*-
import os, sys

sys.path.insert(0, '/var/www/u3172692/data/www/тесткарм.рф/admin_site')
sys.path.insert(1, '/var/www/u3172692/data/djangoenv/lib/python3.9/site-packages')
os.environ['DJANGO_SETTINGS_MODULE'] = 'admin_site.settings'
from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
