from django.conf import settings
from django.db import models

from ..models import *

def write_to_repo_model(model, table_name):
    with open(f'{settings.BASE_DIR}/core/models/storage_models.py', mode='r+') as file:
        all_lines = file.readlines()

        for line in all_lines: #* Overwrite the existing model name (in order to prevent duplications)
            if f"{table_name} = " in line:
                all_lines[all_lines.index(line)] = f"{model} \n"
                file.seek(0)
                file.truncate()
                file.writelines(all_lines)
                break
        else:
            file.write(f"{model} \n")
        file.close()


def delete_repo_model_from_file(table_name):
    with open(f'{settings.BASE_DIR}/core/models/storage_models.py', mode='r+') as file:
        all_lines = file.readlines()

        for line in all_lines: #* Overwrite the existing model name (in order to prevent duplications)
            if f"{table_name} = " in line:
                all_lines[all_lines.index(line)] = f""
                file.seek(0)
                file.truncate()
                file.writelines(all_lines)
                return


def get_field_options(field, table_name):
    """ The Field Option Generator """
    options = {}

    #Base option
    if field.is_unique_key:
        options['unique'] = True
    if field.is_optional:
        options['null'] = True
    if field.default_value:
        options['default'] = f"{field.default_value}"
    if field.is_index:
        options['is_index'] = True

    # if field.data_type in ['STRING', 'TIME', 'DATE', 'DATETIME']:
    #     options['max_length'] = field.length if field.length else 100 #* Specific option for string

    elif field.data_type == "FK": #* Specific option for FK
        if field.reference_entity.table_name == table_name: # Self Relation Field
            options['to'] = f"'{field.reference_entity.table_name}'"
        else:
            options['to'] = f"'{field.reference_entity.table_name}'" 
        options['db_column'] = f"'{field.title}'"
        options['related_name'] = f"'{field.entity.table_name}_{field.title}'"
        options['on_delete'] = f'models.{models.PROTECT.__name__}'

    return options


def load_column_expr(options, type):
    charset_options = ""
    if type in ['STRING','DATE', 'TIME', 'DATETIME', 'NUMCHAR']:
        charset_options = f'models.TextField('

    elif type == "INTEGER":
        charset_options = f'models.IntegerField('

    elif type == "FLOAT":
        charset_options = f'models.FloatField('

    elif type == "BOOL":
        charset_options = f'models.BooleanField('

    elif type == "FK":
        charset_options = f'models.ForeignKey('

    for opt, value in options.items():
        if opt == 'default':
            charset_options += f'{opt}="{value}", '
        else:
            charset_options += f'{opt}={value}, '

    return charset_options + "),"


def create_model_engine(entity_code):
    entity_obj = TableSchema.objects.get(code=entity_code)
    table_name = entity_obj.table_name
    data_structures = TableColumns.objects.filter(entity__code=entity_code, is_active=True)


    base_model_definition = f'{table_name} = type("{table_name}", (BaseBusinessEntity,), {{"__module__": "core.models.storage_models", ' ## The basics of the model

    ## Iterate over DS to make fields
    for field in data_structures:
        options = get_field_options(field=field, table_name=table_name)
        base_model_definition += f"'{field.title}'" + " : " +  load_column_expr(options, field.data_type)

    return base_model_definition + "})", table_name


def create_model_from_ds(entity_code, bulk=False):
    """ Main function of creation model from data strcture"""
    try:
        model, table_name = create_model_engine(entity_code=entity_code)
        write_to_repo_model(model=model, table_name=table_name)
        return True
    except Exception as e:
        print(e)
        return False

