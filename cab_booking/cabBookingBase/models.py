from django.db import models
from django.contrib.auth.models import User
import uuid


# Create your models here.

class cab_category(models.Model):
    cab_model_id = models.UUIDField(unique=True,default=uuid.uuid4)
    category = models.CharField(max_length=200)
    cab_description = models.CharField(max_length=500)
    rate_card = models.IntegerField()


class Cab(models.Model):
    cab_unique_uuid = models.UUIDField(unique=True,default=uuid.uuid4, editable=False)
    cab_license_plate_number = models.CharField(max_length=15)
    cab_model_id = models.ForeignKey(cab_category, on_delete=models.PROTECT)
    cab_owner_id = models.ForeignKey(User, on_delete=models.PROTECT)
    status = models.BooleanField(default=True)

class Payment(models.Model):
    payment_id = models.IntegerField()
    payment_type_name = models.CharField(max_length=20)

class CabBooking(models.Model):
    cab_booking_id = models.CharField(max_length=15,default='UlFQ5eIu4bSOzKe')
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    cab_info = models.ForeignKey(Cab, on_delete=models.PROTECT)
    pickup_date = models.DateField("Date", max_length=20)
    pickup_time_start = models.DateTimeField( max_length=32)
    #end = models.DateTimeField(max_length=32)
    pickup_lat = models.FloatField(null=False,blank=False)
    pickup_lng = models.FloatField(null=False,blank=False)
    drop_lat = models.FloatField(null=False,blank=False)
    drop_lng = models.FloatField(null=False,blank=False)
    status = models.SmallIntegerField(default=1)
    payment_type_id = models.ForeignKey(Payment,on_delete=models.PROTECT)


# class CompanyBase(models.Model):
#     name = models.CharField(blank = False, unique=True,length=200)
#     description  = models.TextField(null= True, blank= True)
#     icon_url = models.URLField(null = True, blank= True)
#
#     def __str__(self):
#         return  self.name
#
#
# class Driver(models.Model):
#     driver_unique_uuid = models.UUIDField(unique=True)
#     driver_name = models.CharField(length=200)
#     dob = models.DateField(max_length=8)
#     driver_license_number = models.CharField(max_length=15)
#     expiry_date = models.DateField(max_length=8)
#     working = models.BooleanField(default=True)
#

#







