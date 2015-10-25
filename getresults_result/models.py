from uuid import uuid4
from django.db import models
from django.utils import timezone
from edc_base.audit_trail import AuditTrail
from edc_base.model.models import BaseUuidModel
from getresults_order.models import Order, Utestid
from getresults_identifier import ResultIdentifier

from .choices import RELEASE_OPTIONS

VALIDATION_STATUS = (
    ('pending', 'Pending'),
    ('partial', 'Partial'),
    ('validated', 'Validated'),
    ('rejected', 'Rejected'),
)

RELEASE_STATUS = (
    ('pending', 'Pending'),
    ('partial', 'Partial'),
    ('released', 'Released'),
    ('rejected', 'Rejected'),
)


RESULT_ITEM_VALIDATION = (
    ('accept', 'Accept'),
    ('reject', 'Reject'),
    ('repeat', 'Repeat'),
    ('ignore', 'Ignore'),
)


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

    last_exported = models.BooleanField(default=False)

    last_exported_datetime = models.DateTimeField(null=True)

    validation_status = models.CharField(
        max_length=10,
        choices=VALIDATION_STATUS,
        default='pending',
        editable=False)

    validation_datetime = models.DateTimeField(null=True)

    release_status = models.CharField(
        max_length=10,
        choices=RELEASE_STATUS,
        default='pending',
        editable=False)

    release_datetime = models.DateTimeField(null=True)

    history = AuditTrail()

    def __str__(self):
        return '{}: {}'.format(self.result_identifier, str(self.order))

    def save(self, *args, **kwargs):
        self.result_identifier = self.result_identifier or ResultIdentifier(self.order.order_identifier)
        super(Result, self).save(*args, **kwargs)

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
        choices=RESULT_ITEM_VALIDATION,
        null=True)

    sender = models.CharField(
        max_length=25,
        null=True,
        help_text='analyzer or instrument')

    source = models.CharField(
        max_length=250,
        null=True,
        help_text='For example, \'filename\' for CSV or \'ASTM\'')

    validated = models.BooleanField(default=False, editable=False)

    validation_datetime = models.DateTimeField(null=True)

    history = AuditTrail()

    def __str__(self):
        return '{}: {}'.format(str(self.utestid), str(self.result))

    class Meta:
        app_label = 'getresults_result'
        db_table = 'getresults_resultitem'
        unique_together = ('result', 'utestid', 'result_datetime')


class Release(BaseUuidModel):

    result = models.ForeignKey(Result)

    release_datetime = models.DateTimeField(
        default=timezone.now)

    status = models.CharField(
        max_length=25,
        choices=RELEASE_OPTIONS)

    comment = models.CharField(
        max_length=25,
        null=True)

    reference = models.CharField(
        max_length=36,
        default=uuid4,
        editable=False)

    history = AuditTrail()

    def __str__(self):
        return '{}: {}'.format(self.result.result_identifier, self.reference)

    def save(self, *args, **kwargs):
        self.released = True if self.release else False
        super(Release, self).save(*args, **kwargs)

    class Meta:
        app_label = 'getresults_result'
        db_table = 'getresults_release'


class Validate(BaseUuidModel):
    """Model to track the validation reference per result item in a result."""

    result_item = models.ForeignKey(ResultItem)

    validate_datetime = models.DateTimeField(
        default=timezone.now)

    status = models.CharField(
        max_length=25,
        # choices=VALIDATE_OPTIONS
    )

    comment = models.CharField(
        max_length=25,
        null=True)

    reference = models.CharField(
        max_length=36,
        default=uuid4,
        editable=False)

    release = models.ForeignKey(Release, null=True, editable=False)

    released = models.BooleanField(default=False)

    history = AuditTrail()

    def __str__(self):
        return '{}: {}'.format(self.result_item.utestid, self.reference)

    def save(self, *args, **kwargs):
        self.released = True if self.release else False
        super(Validate, self).save(*args, **kwargs)

    class Meta:
        app_label = 'getresults_result'
        db_table = 'getresults_validate'
