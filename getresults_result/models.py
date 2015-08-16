from django.db import models

from edc_base.model.models import BaseUuidModel, HistoricalRecords

from getresults_order.models import Order, Utestid

from .choices import RESULT_ITEM_STATUS


class Result(BaseUuidModel):

    result_identifier = models.CharField(
        max_length=25,
        null=True)

    order = models.ForeignKey(Order)

    specimen_identifier = models.CharField(
        max_length=25,
        null=True)

    collection_datetime = models.DateTimeField(null=True)

    status = models.CharField(
        max_length=1,
        null=True)

    analyzer_name = models.CharField(
        max_length=25,
        null=True)

    analyzer_sn = models.CharField(
        max_length=25,
        null=True)

    operator = models.CharField(
        max_length=25,
        null=True)

    validation_reference = models.CharField(
        max_length=25,
        null=True)

    last_exported = models.BooleanField(default=False)

    last_exported_datetime = models.DateTimeField(null=True)

    history = HistoricalRecords()

    def __str__(self):
        return '{}: {}'.format(self.result_identifier, str(self.order))

    class _Meta:
        app_label = 'getresults_result'
        db_table = 'getresults_result'
        unique_together = ('result_identifier', 'collection_datetime')


class ResultItem(BaseUuidModel):

    result = models.ForeignKey(Result)

    utestid = models.ForeignKey(Utestid)

    value = models.CharField(
        max_length=25,
        null=True)

    raw_value = models.CharField(
        max_length=25,
        null=True)

    quantifier = models.CharField(
        max_length=3,
        null=True)

    result_datetime = models.DateTimeField(
        null=True)

    status = models.CharField(
        max_length=10,
        choices=RESULT_ITEM_STATUS,
        null=True)

    validation_reference = models.CharField(
        max_length=25,
        null=True)

    sender = models.CharField(
        max_length=25,
        null=True,
        help_text='analyzer or instrument')

    source = models.CharField(
        max_length=25,
        null=True,
        help_text='For example, \'filename\' for CSV or \'ASTM\'')

    history = HistoricalRecords()

    def __str__(self):
        return '{}: {}'.format(self.utestid, str(self.result))

    class Meta:
        app_label = 'getresults_result'
        db_table = 'getresults_resultitem'
        unique_together = ('result', 'utestid', 'result_datetime')
