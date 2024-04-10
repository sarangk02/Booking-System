# Generated by Django 5.0.3 on 2024-04-09 20:38

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0007_slot_dt'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='slot',
            options={'ordering': ['request_time'], 'verbose_name': 'slot', 'verbose_name_plural': 'slots'},
        ),
        migrations.RemoveField(
            model_name='slot',
            name='dt',
        ),
        migrations.AddField(
            model_name='slot',
            name='is_booked_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='slot',
            name='request_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]