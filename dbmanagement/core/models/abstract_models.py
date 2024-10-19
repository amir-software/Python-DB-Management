from django.db import models

class BaseBusinessEntity(models.Model):
    """ Base model (default fields(table columns) of the created model and )  """
    creation_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    modification_date = models.DateTimeField(auto_now=True, null=True, blank=True)

    deletion_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True