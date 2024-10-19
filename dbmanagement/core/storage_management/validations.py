from ..exceptions import *

from django.apps import apps

TableSchema = apps.get_model(app_label='mojito', model_name='TableSchema')
TableColumns = apps.get_model(app_label='mojito', model_name='TableColumns')

def check_entity_validation(entity_code):
    entity_obj = TableSchema.objects.filter(code=entity_code).first()

    if not entity_obj:
        raise EntityDoesNotExistException
    else:
        if not entity_obj.is_active:
            raise NotActiveEntityException
        if not entity_obj.is_verified:
            raise NotVerifiedEntityException

    return "OK"