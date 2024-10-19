from core.storage_management.model_creation_engine import *

import pytest

@pytest.mark.django_db
class TestFieldOptionGenerator:
    TABLE_NAME = "testcase_person"

    def test_get_field_options_unique(self):
        DATA_STRUCTURE_CODE = "TESTCASE_FARHAM_CODE"
        field_obj = TableColumns.objects.get(code=DATA_STRUCTURE_CODE)

        generated_result = get_field_options(field=field_obj, table_name=self.TABLE_NAME)
        expected_result = {'unique': True}

        assert generated_result == expected_result

    def test_get_field_options_optional(self):
        DATA_STRUCTURE_CODE = "TESTCASE_LAST_SEEN"
        field_obj = TableColumns.objects.get(code=DATA_STRUCTURE_CODE)

        generated_result = get_field_options(field=field_obj, table_name=self.TABLE_NAME)
        expected_result = {'null': True}

        assert generated_result == expected_result

    def test_get_field_options_default(self):
        DATA_STRUCTURE_CODE = "TESTCASE_RANK"
        field_obj = TableColumns.objects.get(code=DATA_STRUCTURE_CODE)

        generated_result = get_field_options(field=field_obj, table_name=self.TABLE_NAME)
        expected_result = {'default': '5.0'}

        assert generated_result == expected_result

    def test_get_field_options_FK(self):
        DATA_STRUCTURE_CODE = "TESTCASE_IDEN_TYPE"
        field_obj = TableColumns.objects.get(code=DATA_STRUCTURE_CODE)

        generated_result = get_field_options(field=field_obj, table_name=self.TABLE_NAME)
        expected_result = {'to': "'testcase_identification_type'", 'db_column': "'identification_type'", 'related_name': "'testcase_person_identification_type'", 'on_delete': 'models.PROTECT'}

        assert generated_result == expected_result

    def test_get_field_options_FK_to_self(self):
        DATA_STRUCTURE_CODE = ""

        assert False


@pytest.mark.django_db
class TestLoadColumnExpression:
    def test_string_types(self,):
        generated_result_string = load_column_expr(options={}, type="STRING")
        generated_result_date = load_column_expr(options={}, type="DATE")
        generated_result_time = load_column_expr(options={}, type="TIME")
        generated_result_datetime = load_column_expr(options={}, type="DATETIME")
        generated_result_numchar = load_column_expr(options={}, type="NUMCHAR")

        expected_result = f'models.TextField(),'

        assert generated_result_string == generated_result_date == generated_result_time == generated_result_datetime == generated_result_numchar \
                == expected_result

    def test_int_type(self):
        generated_result = load_column_expr(options={}, type="INTEGER")
        expected_result = f'models.IntegerField(),'

        assert generated_result == expected_result

    def test_float_type(self):
        generated_result = load_column_expr(options={}, type="FLOAT")
        expected_result = f'models.FloatField(),'

        assert generated_result == expected_result

    def test_bool_type(self):
        generated_result = load_column_expr(options={}, type="BOOL")
        expected_result = f'models.BooleanField(),'

        assert generated_result == expected_result

    def test_fk_type(self):
        generated_result = load_column_expr(options={}, type="FK")
        expected_result = f'models.ForeignKey(),'

        assert generated_result == expected_result

    def test_column_with_options(self):
        pass