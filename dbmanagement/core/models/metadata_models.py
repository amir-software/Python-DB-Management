from django.db import models


class TableColumns(models.Model):
    data_type_choices = (
        ('STRING' , 'string'),
        ('INTEGER' , 'integer'),
        ('FK' , 'foreign_key'),
        ('BOOL' , 'bool'),
        ('FLOAT' , 'float'),
        ('TIME' , 'time'),
        ('DATE' , 'date'),
        ('DATETIME' , 'datetime'),
        ('NUMCHAR' , 'numchar'),
    )
    table_schema = models.ForeignKey('TableSchema',
                               on_delete=models.CASCADE, 
                               db_column='entity',
                               null=True,
                               blank=True,)

    code = models.CharField('شناسه', null=True, max_length=100)

    title = models.CharField(max_length=100,null=True)
    

    length = models.IntegerField(null=True,blank=True)

    data_type = models.CharField(max_length=100, choices=data_type_choices)

    reference_table = models.ForeignKey('TableSchema',
                                on_delete=models.PROTECT,
                                db_column = 'fk_entity',
                                null=True,
                                blank=True,
                                related_name='+',)


    is_optional = models.BooleanField(default=True)
    
    is_unique_key = models.BooleanField(default=False)

    is_primary_key = models.BooleanField('Primary Key',default=False)

    is_index = models.BooleanField(default=False)
                           
    class Meta:
        unique_together = (('title', 'entity',), ('code', 'entity',))


    def __str__(self) -> str:
        return self.title


class TableSchema(models.Model):
    DB_STATUS_CHOICES = (
        ('READY_TO_CREATE_MODEL', 'آماده ساخت مدل'),
        ('READY_TO_UPDATE', 'آماده بروزرسانی جدول'),
        ('MODEL_CREATED', 'مدل ساخته شد.'),
        ('TABLE_CREATED', 'جدول ساخته شد.'),
    )

    code = models.CharField(null=True,max_length=100, unique=True)

    title = models.CharField(max_length=200)

    table_name = models.CharField('نام مدل', max_length=200, unique=True)

    is_active = models.BooleanField('فعال است', null=True,blank=True, default=True)

    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    date_modified = models.DateTimeField(auto_now=True, null=True, blank=True)

    date_removed = models.DateTimeField(null=True, blank=True)

    db_status = models.CharField(max_length=100, default='READY_TO_CREATE_MODEL')

    def __str__(self):
        if self.title:
            return self.title
        else:
            return self.id