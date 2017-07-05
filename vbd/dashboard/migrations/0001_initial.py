# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Operation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=512)),
                ('start_command', models.CharField(max_length=512, null=True, blank=True)),
                ('stop_command', models.CharField(max_length=512, null=True, blank=True)),
                ('description', models.CharField(max_length=1024, null=True, blank=True)),
            ],
            options={
                'db_table': 'operation',
            },
        ),
        migrations.CreateModel(
            name='OperationGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=60)),
                ('sort_key', models.IntegerField(unique=True)),
            ],
            options={
                'ordering': ['-sort_key'],
                'db_table': 'operation_group',
            },
        ),
        migrations.CreateModel(
            name='ServiceStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status_cmd', models.CharField(max_length=512, null=True, blank=True)),
                ('status_cmd_type', models.CharField(default=b'Http', max_length=100, choices=[(b'Shell', b'Shell'), (b'Http', b'Http')])),
                ('status_cmd_timeout', models.IntegerField(default=120)),
                ('status_flag', models.BooleanField(default=False, choices=[(True, b'Running'), (False, b'Stopped')])),
                ('status_response', models.CharField(max_length=1024, null=True, blank=True)),
            ],
            options={
                'db_table': 'service_status',
            },
        ),
        migrations.CreateModel(
            name='VEXGolbalSettings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('kubectl_ip_address', models.GenericIPAddressField(null=True, blank=True)),
                ('grafana_http_address', models.CharField(max_length=128, null=True, blank=True)),
                ('use_default_version', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'vex_global_settings',
            },
        ),
        migrations.CreateModel(
            name='VEXOperation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=512)),
                ('start_command', models.CharField(max_length=512, null=True, blank=True)),
                ('stop_command', models.CharField(max_length=512, null=True, blank=True)),
                ('description', models.CharField(max_length=1024, null=True, blank=True)),
                ('deploy_command', models.CharField(max_length=512)),
                ('build_info', models.CharField(max_length=512, null=True, blank=True)),
                ('running_version', models.CharField(max_length=512, null=True, blank=True)),
            ],
            options={
                'db_table': 'deploy_operation',
            },
        ),
        migrations.CreateModel(
            name='VEXVersion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('version', models.CharField(unique=True, max_length=100)),
                ('is_default', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['version'],
                'db_table': 'vex_version',
                'get_latest_by': 'version',
            },
        ),
        migrations.AddField(
            model_name='vexoperation',
            name='deploy_version',
            field=models.ForeignKey(blank=True, to='dashboard.VEXVersion', null=True),
        ),
        migrations.AddField(
            model_name='vexoperation',
            name='status',
            field=models.OneToOneField(null=True, blank=True, to='dashboard.ServiceStatus'),
        ),
        migrations.AddField(
            model_name='operation',
            name='group',
            field=models.ForeignKey(blank=True, to='dashboard.OperationGroup', null=True),
        ),
        migrations.AddField(
            model_name='operation',
            name='status',
            field=models.OneToOneField(null=True, blank=True, to='dashboard.ServiceStatus'),
        ),
    ]
