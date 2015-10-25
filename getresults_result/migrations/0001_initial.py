# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import edc_base.model.fields.hostname_modification_field
from django.conf import settings
import django.db.models.deletion
import edc_base.model.fields.uuid_auto_field
import django.db.models.fields
import django.utils.timezone
import django_revision.revision_field
import uuid
import edc_base.model.fields.userfield
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('getresults_order', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalRelease',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.db.models.fields.NOT_PROVIDED, auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, default=django.db.models.fields.NOT_PROVIDED, verbose_name='modified')),
                ('user_created', edc_base.model.fields.userfield.UserField(max_length=50, editable=False, verbose_name='user created')),
                ('user_modified', edc_base.model.fields.userfield.UserField(max_length=50, editable=False, verbose_name='user modified')),
                ('hostname_created', models.CharField(help_text='System field. (modified on create only)', max_length=50, editable=False, default='mac2-2.local')),
                ('hostname_modified', edc_base.model.fields.hostname_modification_field.HostnameModificationField(help_text='System field. (modified on every save)', max_length=50, editable=False)),
                ('revision', django_revision.revision_field.RevisionField(help_text='System field. Git repository tag:branch:commit.', verbose_name='Revision', editable=False, null=True, blank=True, max_length=75)),
                ('id', edc_base.model.fields.uuid_auto_field.UUIDAutoField(help_text='System field. UUID primary key.', db_index=True, editable=False)),
                ('release_datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.CharField(choices=[('OK', 'Release'), ('XOK', 'Do not release')], max_length=25)),
                ('comment', models.CharField(null=True, max_length=25)),
                ('reference', models.CharField(max_length=36, editable=False, default=uuid.uuid4)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL, null=True, on_delete=django.db.models.deletion.SET_NULL)),
            ],
            options={
                'verbose_name': 'historical release',
                'get_latest_by': 'history_date',
                'ordering': ('-history_date', '-history_id'),
            },
        ),
        migrations.CreateModel(
            name='HistoricalResult',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.db.models.fields.NOT_PROVIDED, auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, default=django.db.models.fields.NOT_PROVIDED, verbose_name='modified')),
                ('user_created', edc_base.model.fields.userfield.UserField(max_length=50, editable=False, verbose_name='user created')),
                ('user_modified', edc_base.model.fields.userfield.UserField(max_length=50, editable=False, verbose_name='user modified')),
                ('hostname_created', models.CharField(help_text='System field. (modified on create only)', max_length=50, editable=False, default='mac2-2.local')),
                ('hostname_modified', edc_base.model.fields.hostname_modification_field.HostnameModificationField(help_text='System field. (modified on every save)', max_length=50, editable=False)),
                ('revision', django_revision.revision_field.RevisionField(help_text='System field. Git repository tag:branch:commit.', verbose_name='Revision', editable=False, null=True, blank=True, max_length=75)),
                ('id', edc_base.model.fields.uuid_auto_field.UUIDAutoField(help_text='System field. UUID primary key.', db_index=True, editable=False)),
                ('result_identifier', models.CharField(null=True, max_length=25)),
                ('specimen_identifier', models.CharField(null=True, max_length=25)),
                ('collection_datetime', models.DateTimeField(null=True)),
                ('status', models.CharField(null=True, max_length=1)),
                ('analyzer_name', models.CharField(null=True, max_length=25)),
                ('analyzer_sn', models.CharField(null=True, max_length=25)),
                ('operator', models.CharField(null=True, max_length=25)),
                ('last_exported', models.BooleanField(default=False)),
                ('last_exported_datetime', models.DateTimeField(null=True)),
                ('validation_status', models.CharField(max_length=10, choices=[('pending', 'Pending'), ('partial', 'Partial'), ('validated', 'Validated'), ('rejected', 'Rejected')], editable=False, default='pending')),
                ('release_status', models.CharField(max_length=10, choices=[('pending', 'Pending'), ('partial', 'Partial'), ('released', 'Released'), ('rejected', 'Rejected')], editable=False, default='pending')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL, null=True, on_delete=django.db.models.deletion.SET_NULL)),
                ('order', models.ForeignKey(related_name='+', db_constraint=False, to='getresults_order.Order', null=True, blank=True, on_delete=django.db.models.deletion.DO_NOTHING)),
            ],
            options={
                'verbose_name': 'historical result',
                'get_latest_by': 'history_date',
                'ordering': ('-history_date', '-history_id'),
            },
        ),
        migrations.CreateModel(
            name='HistoricalResultItem',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.db.models.fields.NOT_PROVIDED, auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, default=django.db.models.fields.NOT_PROVIDED, verbose_name='modified')),
                ('user_created', edc_base.model.fields.userfield.UserField(max_length=50, editable=False, verbose_name='user created')),
                ('user_modified', edc_base.model.fields.userfield.UserField(max_length=50, editable=False, verbose_name='user modified')),
                ('hostname_created', models.CharField(help_text='System field. (modified on create only)', max_length=50, editable=False, default='mac2-2.local')),
                ('hostname_modified', edc_base.model.fields.hostname_modification_field.HostnameModificationField(help_text='System field. (modified on every save)', max_length=50, editable=False)),
                ('revision', django_revision.revision_field.RevisionField(help_text='System field. Git repository tag:branch:commit.', verbose_name='Revision', editable=False, null=True, blank=True, max_length=75)),
                ('id', edc_base.model.fields.uuid_auto_field.UUIDAutoField(help_text='System field. UUID primary key.', db_index=True, editable=False)),
                ('value', models.CharField(null=True, max_length=25)),
                ('raw_value', models.CharField(null=True, max_length=25)),
                ('quantifier', models.CharField(null=True, max_length=3)),
                ('result_datetime', models.DateTimeField(null=True)),
                ('status', models.CharField(null=True, choices=[('accept', 'Accept'), ('reject', 'Reject'), ('repeat', 'Repeat'), ('ignore', 'Ignore')], max_length=10)),
                ('sender', models.CharField(help_text='analyzer or instrument', null=True, max_length=25)),
                ('source', models.CharField(help_text="For example, 'filename' for CSV or 'ASTM'", null=True, max_length=250)),
                ('validated', models.BooleanField(editable=False, default=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL, null=True, on_delete=django.db.models.deletion.SET_NULL)),
            ],
            options={
                'verbose_name': 'historical result item',
                'get_latest_by': 'history_date',
                'ordering': ('-history_date', '-history_id'),
            },
        ),
        migrations.CreateModel(
            name='HistoricalValidate',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.db.models.fields.NOT_PROVIDED, auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, default=django.db.models.fields.NOT_PROVIDED, verbose_name='modified')),
                ('user_created', edc_base.model.fields.userfield.UserField(max_length=50, editable=False, verbose_name='user created')),
                ('user_modified', edc_base.model.fields.userfield.UserField(max_length=50, editable=False, verbose_name='user modified')),
                ('hostname_created', models.CharField(help_text='System field. (modified on create only)', max_length=50, editable=False, default='mac2-2.local')),
                ('hostname_modified', edc_base.model.fields.hostname_modification_field.HostnameModificationField(help_text='System field. (modified on every save)', max_length=50, editable=False)),
                ('revision', django_revision.revision_field.RevisionField(help_text='System field. Git repository tag:branch:commit.', verbose_name='Revision', editable=False, null=True, blank=True, max_length=75)),
                ('id', edc_base.model.fields.uuid_auto_field.UUIDAutoField(help_text='System field. UUID primary key.', db_index=True, editable=False)),
                ('validate_datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.CharField(max_length=25)),
                ('comment', models.CharField(null=True, max_length=25)),
                ('reference', models.CharField(max_length=36, editable=False, default=uuid.uuid4)),
                ('released', models.BooleanField(default=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(related_name='+', to=settings.AUTH_USER_MODEL, null=True, on_delete=django.db.models.deletion.SET_NULL)),
            ],
            options={
                'verbose_name': 'historical validate',
                'get_latest_by': 'history_date',
                'ordering': ('-history_date', '-history_id'),
            },
        ),
        migrations.CreateModel(
            name='Release',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.db.models.fields.NOT_PROVIDED, auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, default=django.db.models.fields.NOT_PROVIDED, verbose_name='modified')),
                ('user_created', edc_base.model.fields.userfield.UserField(max_length=50, editable=False, verbose_name='user created')),
                ('user_modified', edc_base.model.fields.userfield.UserField(max_length=50, editable=False, verbose_name='user modified')),
                ('hostname_created', models.CharField(help_text='System field. (modified on create only)', max_length=50, editable=False, default='mac2-2.local')),
                ('hostname_modified', edc_base.model.fields.hostname_modification_field.HostnameModificationField(help_text='System field. (modified on every save)', max_length=50, editable=False)),
                ('revision', django_revision.revision_field.RevisionField(help_text='System field. Git repository tag:branch:commit.', verbose_name='Revision', editable=False, null=True, blank=True, max_length=75)),
                ('id', edc_base.model.fields.uuid_auto_field.UUIDAutoField(help_text='System field. UUID primary key.', primary_key=True, editable=False, serialize=False)),
                ('release_datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.CharField(choices=[('OK', 'Release'), ('XOK', 'Do not release')], max_length=25)),
                ('comment', models.CharField(null=True, max_length=25)),
                ('reference', models.CharField(max_length=36, editable=False, default=uuid.uuid4)),
            ],
            options={
                'db_table': 'getresults_release',
            },
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.db.models.fields.NOT_PROVIDED, auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, default=django.db.models.fields.NOT_PROVIDED, verbose_name='modified')),
                ('user_created', edc_base.model.fields.userfield.UserField(max_length=50, editable=False, verbose_name='user created')),
                ('user_modified', edc_base.model.fields.userfield.UserField(max_length=50, editable=False, verbose_name='user modified')),
                ('hostname_created', models.CharField(help_text='System field. (modified on create only)', max_length=50, editable=False, default='mac2-2.local')),
                ('hostname_modified', edc_base.model.fields.hostname_modification_field.HostnameModificationField(help_text='System field. (modified on every save)', max_length=50, editable=False)),
                ('revision', django_revision.revision_field.RevisionField(help_text='System field. Git repository tag:branch:commit.', verbose_name='Revision', editable=False, null=True, blank=True, max_length=75)),
                ('id', edc_base.model.fields.uuid_auto_field.UUIDAutoField(help_text='System field. UUID primary key.', primary_key=True, editable=False, serialize=False)),
                ('result_identifier', models.CharField(null=True, max_length=25)),
                ('specimen_identifier', models.CharField(null=True, max_length=25)),
                ('collection_datetime', models.DateTimeField(null=True)),
                ('status', models.CharField(null=True, max_length=1)),
                ('analyzer_name', models.CharField(null=True, max_length=25)),
                ('analyzer_sn', models.CharField(null=True, max_length=25)),
                ('operator', models.CharField(null=True, max_length=25)),
                ('last_exported', models.BooleanField(default=False)),
                ('last_exported_datetime', models.DateTimeField(null=True)),
                ('validation_status', models.CharField(max_length=10, choices=[('pending', 'Pending'), ('partial', 'Partial'), ('validated', 'Validated'), ('rejected', 'Rejected')], editable=False, default='pending')),
                ('release_status', models.CharField(max_length=10, choices=[('pending', 'Pending'), ('partial', 'Partial'), ('released', 'Released'), ('rejected', 'Rejected')], editable=False, default='pending')),
                ('order', models.ForeignKey(to='getresults_order.Order')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ResultItem',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.db.models.fields.NOT_PROVIDED, auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, default=django.db.models.fields.NOT_PROVIDED, verbose_name='modified')),
                ('user_created', edc_base.model.fields.userfield.UserField(max_length=50, editable=False, verbose_name='user created')),
                ('user_modified', edc_base.model.fields.userfield.UserField(max_length=50, editable=False, verbose_name='user modified')),
                ('hostname_created', models.CharField(help_text='System field. (modified on create only)', max_length=50, editable=False, default='mac2-2.local')),
                ('hostname_modified', edc_base.model.fields.hostname_modification_field.HostnameModificationField(help_text='System field. (modified on every save)', max_length=50, editable=False)),
                ('revision', django_revision.revision_field.RevisionField(help_text='System field. Git repository tag:branch:commit.', verbose_name='Revision', editable=False, null=True, blank=True, max_length=75)),
                ('id', edc_base.model.fields.uuid_auto_field.UUIDAutoField(help_text='System field. UUID primary key.', primary_key=True, editable=False, serialize=False)),
                ('value', models.CharField(null=True, max_length=25)),
                ('raw_value', models.CharField(null=True, max_length=25)),
                ('quantifier', models.CharField(null=True, max_length=3)),
                ('result_datetime', models.DateTimeField(null=True)),
                ('status', models.CharField(null=True, choices=[('accept', 'Accept'), ('reject', 'Reject'), ('repeat', 'Repeat'), ('ignore', 'Ignore')], max_length=10)),
                ('sender', models.CharField(help_text='analyzer or instrument', null=True, max_length=25)),
                ('source', models.CharField(help_text="For example, 'filename' for CSV or 'ASTM'", null=True, max_length=250)),
                ('validated', models.BooleanField(editable=False, default=False)),
                ('result', models.ForeignKey(to='getresults_result.Result')),
                ('utestid', models.ForeignKey(to='getresults_order.Utestid')),
            ],
            options={
                'db_table': 'getresults_resultitem',
            },
        ),
        migrations.CreateModel(
            name='Validate',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.db.models.fields.NOT_PROVIDED, auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, default=django.db.models.fields.NOT_PROVIDED, verbose_name='modified')),
                ('user_created', edc_base.model.fields.userfield.UserField(max_length=50, editable=False, verbose_name='user created')),
                ('user_modified', edc_base.model.fields.userfield.UserField(max_length=50, editable=False, verbose_name='user modified')),
                ('hostname_created', models.CharField(help_text='System field. (modified on create only)', max_length=50, editable=False, default='mac2-2.local')),
                ('hostname_modified', edc_base.model.fields.hostname_modification_field.HostnameModificationField(help_text='System field. (modified on every save)', max_length=50, editable=False)),
                ('revision', django_revision.revision_field.RevisionField(help_text='System field. Git repository tag:branch:commit.', verbose_name='Revision', editable=False, null=True, blank=True, max_length=75)),
                ('id', edc_base.model.fields.uuid_auto_field.UUIDAutoField(help_text='System field. UUID primary key.', primary_key=True, editable=False, serialize=False)),
                ('validate_datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.CharField(max_length=25)),
                ('comment', models.CharField(null=True, max_length=25)),
                ('reference', models.CharField(max_length=36, editable=False, default=uuid.uuid4)),
                ('released', models.BooleanField(default=False)),
                ('release', models.ForeignKey(to='getresults_result.Release', editable=False, null=True)),
                ('result_item', models.ForeignKey(to='getresults_result.ResultItem')),
            ],
            options={
                'db_table': 'getresults_validate',
            },
        ),
        migrations.AddField(
            model_name='release',
            name='result',
            field=models.ForeignKey(to='getresults_result.Result'),
        ),
        migrations.AddField(
            model_name='historicalvalidate',
            name='release',
            field=models.ForeignKey(related_name='+', db_constraint=False, to='getresults_result.Release', null=True, blank=True, on_delete=django.db.models.deletion.DO_NOTHING),
        ),
        migrations.AddField(
            model_name='historicalvalidate',
            name='result_item',
            field=models.ForeignKey(related_name='+', db_constraint=False, to='getresults_result.ResultItem', null=True, blank=True, on_delete=django.db.models.deletion.DO_NOTHING),
        ),
        migrations.AddField(
            model_name='historicalresultitem',
            name='result',
            field=models.ForeignKey(related_name='+', db_constraint=False, to='getresults_result.Result', null=True, blank=True, on_delete=django.db.models.deletion.DO_NOTHING),
        ),
        migrations.AddField(
            model_name='historicalresultitem',
            name='utestid',
            field=models.ForeignKey(related_name='+', db_constraint=False, to='getresults_order.Utestid', null=True, blank=True, on_delete=django.db.models.deletion.DO_NOTHING),
        ),
        migrations.AddField(
            model_name='historicalrelease',
            name='result',
            field=models.ForeignKey(related_name='+', db_constraint=False, to='getresults_result.Result', null=True, blank=True, on_delete=django.db.models.deletion.DO_NOTHING),
        ),
        migrations.AlterUniqueTogether(
            name='resultitem',
            unique_together=set([('result', 'utestid', 'result_datetime')]),
        ),
    ]
