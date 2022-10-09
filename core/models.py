from django.db import models
from . import managers

# Create your models here.


class TimeStampedModel(models.Model):

    """Time Stamped Model"""

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = managers.CustomModelManager()
    # DB에 등륵되지 않게 하는 Property인 abstract
    class Meta:
        abstract = True
