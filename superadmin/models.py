from django.db import models

from generic.custom_model import GenericBaseModel


# Create your models here.
class HomeModel(GenericBaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    form_template = models.CharField(max_length=255)
    entity = models.CharField(max_length=255)
    width = models.IntegerField()
