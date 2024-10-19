from .model_creation_engine import create_model_from_ds
from .migration_engine import apply_makemigrations, apply_migrate
from .validations import check_entity_validation

from django.conf import settings

from rest_framework.response import Response
from rest_framework import status as status_codes
from rest_framework.views import APIView

import time, os


class RepositoryManager(APIView):
    """ Create database schema (django model) for persisting tables in database. """
    def post(self, request, *args, **kwargs):
        data =request.data

        entity_code = data.get('entity_code')
        if check_entity_validation(entity_code=entity_code) != "OK":
            return check_entity_validation(entity_code=entity_code)

        status = create_model_from_ds(entity_code=entity_code)

        os.system(f'sudo systemctl restart {settings.GUNICORN_SERVICE_NAME}')
        time.sleep(1)
        return Response({'STATUS' : status}, status=status_codes.HTTP_200_OK)


class PersistTable(APIView):
    def post(self, request, *args, **kwargs):
        """ Persist all the table needed into database. """
        data = request.data

        entity_code = data.get('entity_code')
        if check_entity_validation(entity_code=entity_code) != "OK":
            return check_entity_validation(entity_code=entity_code)
        try:
            apply_makemigrations()
            apply_migrate()
            return Response({'STATUS' : 'SUCCESS'}, status=status_codes.HTTP_200_OK)
        except:
            return Response({'STATUS' : 'FAIL', 'message' : 'could not persist table, please check out the data structure'}, status=status_codes.HTTP_400_BAD_REQUEST)