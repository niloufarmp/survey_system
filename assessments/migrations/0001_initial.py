# Generated by Django 3.1.2 on 2020-10-19 02:50

import uuid

import django.db.models.deletion
import jsonfield.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Assessment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('UUID', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('score_formula', models.CharField(max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Submit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.FloatField(blank=True)),
                ('answers', jsonfield.fields.JSONField(default=dict)),
                ('error', models.CharField(max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('assessment',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assessments.assessment',
                                   to_field='UUID')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('assessment',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assessments.assessment',
                                   to_field='UUID')),
            ],
        ),
    ]