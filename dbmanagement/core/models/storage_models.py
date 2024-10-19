from django.db.models.signals import class_prepared, pre_init


def add_db_prefix(sender, **kwargs):
    """ Removing the prefix of the persited tables"""
    prefixes = ['core_',] 

    for prefix in prefixes:
        if prefix in sender._meta.db_table:
            sender._meta.db_table = sender._meta.db_table.replace(prefix, "")

pre_init.connect(add_db_prefix)
class_prepared.connect(add_db_prefix)

