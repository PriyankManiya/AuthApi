from django.db import models
from django.contrib.postgres.fields import ArrayField

# from djangoAuthApi.djangoAuthApi import settings

from djangoAuthApi import settings
# Create your models here.


class Notes(models.Model):
    msg = models.TextField()
    notecreatorid = models.ForeignKey(
        settings.AUTH_USER_MODEL, models.DO_NOTHING, db_column='notecreatorid', related_name='notecreatorid')
    isactive = models.BooleanField(default=True)
    createdat = models.DateTimeField(auto_now_add=True)
    updatedat = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'notes'


class Tickets(models.Model):
    creatorid = models.ForeignKey(
        settings.AUTH_USER_MODEL, models.DO_NOTHING, db_column='creatorid', related_name='creatorid')
    resolverid = models.ForeignKey(
        settings.AUTH_USER_MODEL, models.DO_NOTHING, db_column='resolverid', related_name='resolverid')
    # ticket_note = ArrayField(
    #     models.ForeignKey(
    #         Notes, models.DO_NOTHING, db_column='ticket_note', related_name='ticket_note'))

    isresolved = models.BooleanField(default=False)

    resolveddate = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    REQUIRED_FIELDS = ['creatorid', 'resolverid', 'isresolved', 'resolveddate']

    class Meta:
        managed = False
        db_table = 'tickets'
