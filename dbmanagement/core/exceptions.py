from rest_framework.exceptions import APIException

class EntityDoesNotExistException(APIException):
    status_code = 400
    default_detail = 'موجودیتی با این کد وجود ندارد'
    default_code = 'entity_doesnot_exist'


class NotVerifiedEntityException(APIException):
    status_code = 403
    default_detail = 'موجودیت معتبر نمیباشد.'
    default_code = 'verified_entity_required'


class NotActiveEntityException(APIException):
    status_code = 403
    default_detail = 'موجودیت فعال نمیباشد.'
    default_code = 'active_entity_required'


class CouldNotDeleteCreatedTableSchema(APIException):
    status_code = 403
    default_detail = 'موجودیت هایی که در جدول ساخته شده اند و دارای رکورد هستند اجازه حذف ندارند.میتوانید آنرا غیر فعال کنید.'
    default_code = 'could_not_delete_created_repository_entity'