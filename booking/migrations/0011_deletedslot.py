# Generated by Django 5.0.3 on 2024-04-12 17:45

import booking.models
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0010_alter_slot_payment_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeletedSlot',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('payment_image', models.ImageField(blank=True, null=True, upload_to=booking.models.DeletedSlot.payment_image_path)),
                ('request_time', models.DateTimeField(editable=False)),
                ('deletiontime', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('reason', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Deleted Slot',
                'verbose_name_plural': 'Deleted Slots',
                'ordering': ['request_time'],
            },
        ),
    ]
