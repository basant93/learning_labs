# Generated by Django 2.1.1 on 2018-09-16 12:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cabBookingBase', '0002_driver_paymentdetails'),
    ]

    operations = [
        migrations.AddField(
            model_name='driver',
            name='cab_driver',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.PROTECT, to='cabBookingBase.Cab'),
        ),
        migrations.AlterField(
            model_name='driver',
            name='driver_booking',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.PROTECT, to='cabBookingBase.CabBooking'),
        ),
        migrations.AlterField(
            model_name='driver',
            name='driver_name',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='paymentdetails',
            name='fare',
            field=models.IntegerField(default=40),
        ),
    ]
