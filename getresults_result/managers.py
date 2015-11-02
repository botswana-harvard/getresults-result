from django.db import models
from getresults_result.constants import VALIDATED, RELEASED, CANCELLED, PARTIAL, PENDING, REPEATED


class ResultManager(models.Manager):

    def unvalidated(self):
        return self.filter(validation_status__in=[PENDING, PARTIAL]).order_by(
            'created', 'result_identifier')

    def validated(self):
        return self.filter(validation_status__in=[VALIDATED, CANCELLED, REPEATED])

    def unreleased(self):
        return self.validated().exclude(
            release_status__in=[RELEASED, CANCELLED, REPEATED]
        ).order_by('validation_datetime', 'result_identifier')

    def released(self):
        return self.validated().filter(release_status__in=[RELEASED, CANCELLED, REPEATED])

    def unvalidated_previous(self, created, options=None):
        options = options or {}
        return self.unvalidated().filter(
            created__lt=created, **options).order_by(
                '-created', 'result_identifier')

    def unvalidated_next(self, created, options=None):
        options = options or {}
        return self.unvalidated().filter(
            created__gt=created, **options).order_by(
                'created', 'result_identifier')

    def unreleased_previous(self, validation_datetime, options=None):
        options = options or {}
        return self.unreleased().filter(
            validation_datetime__lt=validation_datetime, **options).order_by(
                '-validation_datetime', 'result_identifier')

    def unreleased_next(self, validation_datetime, options=None):
        options = options or {}
        return self.unreleased().filter(
            validation_datetime__gt=validation_datetime,
            **options).order_by(
                'validation_datetime', 'result_identifier')
