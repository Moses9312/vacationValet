"""
WSGI config for hrApp project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hrApp.settings")

application = get_wsgi_application()

# """
# WSGI config for hrApp project.
#
# It exposes the WSGI callable as a module-level variable named ``application``.
#
# For more information on this file, see
# https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
# """
#
# import os
# import sys
#
# # Adăugați calea directorului proiectului dvs. dacă nu este deja în sys.path
# path = '/path/to/Users/cristianmoise/PycharmProjects/vacationValet'
# if path not in sys.path:
#     sys.path.append(path)
#
# # Activarea mediului virtual
# activate_this = '/home/username/PycharmProjects/vacationValet/.venv/bin/activate_this.py'
# with open(activate_this) as file_:
#     exec(file_.read(), dict(__file__=activate_this))
#
# from django.core.wsgi import get_wsgi_application
#
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hrApp.settings")
#
# application = get_wsgi_application()




