from django.core.management import call_command
from django.conf import settings

import os, time


def apply_makemigrations(app="core"):
    call_command("makemigrations", app)
    os.system(f'sudo systemctl restart {settings.GUNICORN_SERVICE_NAME}')
    time.sleep(1)


def apply_migrate(app="core", database="storage"):
    call_command('migrate', app, database=database)