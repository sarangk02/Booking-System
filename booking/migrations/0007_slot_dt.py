# Generated by Django 5.0.3 on 2024-04-09 20:07

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0006_remove_customuser_last_login_slot'),
    ]

    operations = [
        migrations.AddField(
            model_name='slot',
            name='dt',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
