from uuid import uuid4
from django.db import models
from django.utils import timezone
from edc_base.audit_trail import AuditTrail
from edc_base.model.models import BaseUuidModel
from getresults_order.models import Order, Utestid
from getresults_identifier import ResultIdentifier

from .choices import RELEASE_OPTIONS
from .constants import ACCEPT, CANCEL, REPEAT, IGNORE, PENDING, PARTIAL, VALIDATED, CANCELLED, RELEASED
from getresults_result.constants import RELEASE, REVIEW, REPEATED
from getresults_result.managers import ResultManager

VALIDATION_STATUS = (
    (PENDING, 'Pending'),
    (PARTIAL, 'Partial'),  # set by system if some result items accepted/cancelled but not all
    (VALIDATED, 'Validated'),  # set by system if all result items accepted/cancelled
    (CANCELLED, 'Cancelled'),  # set by system if all result items cancelled
)

RELEASE_STATUS = (
    (PENDING, 'Pending'),
    (PARTIAL, 'Partial'),  # set by user if some accepted/cancelled AND some to be repeated
    (RELEASED, 'Released'),  # set by user if all accepted/cancelled
    (REPEATED, 'Repeated'),  # set by system if all cancelled
    (CANCELLED, 'Cancelled'),  # set by system if all cancelled
)


RESULT_ITEM_VALIDATION = (
    (ACCEPT, 'Accept'),  # flags order item as complete
    (REPEAT, 'Repeat'),  # flags order item ???
    (CANCEL, 'Cancel'),  # flags order item as cancelled
    (IGNORE, 'Ignore'),  # does nothing
    (PENDING, 'Pending'),  # initial state
)


RESULT_ITEM_RELEASE = (
    (PENDING, 'Pending'),  # set by no action or ignore
    ('release', 'Release'),  # set by user if accepted
    (REPEAT, 'Repeat'),  # set by system if repeat
    (CANCEL, 'Cancel'),  # set by system if cancel
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
        null=True,
        blank=True)

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

    last_exported_datetime = models.DateTimeField(null=True, blank=True)

    validation_status = models.CharField(
        max_length=10,
        choices=VALIDATION_STATUS,
        default=PENDING)

    validation_datetime = models.DateTimeField(null=True, blank=True)

    release_status = models.CharField(
        max_length=10,
        choices=RELEASE_STATUS,
        default=PENDING)

    release_datetime = models.DateTimeField(null=True, blank=True)

    objects = ResultManager()

    history = AuditTrail()

    def __str__(self):
        return '{}: {}'.format(self.result_identifier, str(self.order))

    def save(self, *args, **kwargs):
        self.result_identifier = self.result_identifier or ResultIdentifier(self.order.order_identifier)
        super(Result, self).save(*args, **kwargs)

    def get_validation_status(self, result_items):
        lst = []
        for result_item in result_items:
            lst.append(result_item.status)
        if all([l == ACCEPT for l in lst]):
            return VALIDATED
        elif all([l == CANCEL for l in lst]):
            return CANCELLED
        elif all([l == REPEAT for l in lst]):
            return REPEATED
        elif all([l == IGNORE for l in lst]):
            return PENDING
        elif any([l == ACCEPT for l in lst]):
            return PARTIAL
        else:
            return PENDING

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
        default=PENDING)

    sender = models.CharField(
        max_length=25,
        null=True,
        help_text='analyzer or instrument')

    source = models.CharField(
        max_length=250,
        null=True,
        help_text='For example, \'filename\' for CSV or \'ASTM\'')

    validation_comment = models.CharField(
        max_length=25,
        null=True,
        blank=True)

    validation_datetime = models.DateTimeField(null=True)

    release_status = models.CharField(
        max_length=10,
        choices=RELEASE_OPTIONS,
        null=True)

    release_datetime = models.DateTimeField(null=True, blank=True)

    comment = models.CharField(
        max_length=100,
        null=True,
        blank=True)

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
        max_length=25, blank=True,
        choices=RELEASE_OPTIONS)

    comment = models.CharField(
        max_length=25,
        null=True,
        blank=True)

    reference = models.CharField(
        max_length=36,
        default=uuid4,
        editable=False)

    history = AuditTrail()

    def __str__(self):
        return '{}: {}'.format(self.result.result_identifier, self.reference)

    def update_result(self):
        if self.status == RELEASE:
            self.result.release_status = RELEASED
            self.result.release_datetime = timezone.now()
        elif self.status == REVIEW:
            self.result.validation_status = REVIEW
            self.result.release_datetime = None
        elif self.status == CANCELLED:
            self.result.release_status = RELEASED
            self.result.release_datetime = timezone.now()
        else:
            self.result.release_status = PENDING
            self.result.release_datetime = None
        self.result.save()
        return self.result

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
        null=True,
        blank=True)

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
