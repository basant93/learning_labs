from django.db import models
import uuid

# Create your models here.




class CompanyBase(models.Model):
    name = models.CharField(blank = False, unique=True,length=200)
    description  = models.TextField(null= True, blank= True)
    icon_url = models.URLField(null = True, blank= True)

    def __str__(self):
        return  self.name


class Driver(models.Model):
    driver_unique_uuid = models.UUIDField(unique=True)
    driver_name = models.CharField(length=200)
    dob = models.DateField(max_length=8)
    driver_license_number = models.CharField(max_length=15)
    expiry_date = models.DateField(max_length=8)
    working = models.BooleanField(default=True)

class Cab(models.Model):
    cab_unique_uuid = models.UUIDField(unique=True,default=uuid.uuid4, editable=False)
    cab_license_plate_number = models.CharField(max_length=15)
    cab_model_id = models.IntegerField()
    cab_owner_id = models.IntegerField()
    status = models.BooleanField(default=True)

class cab_category(models.Model):
    category = models.CharField(length=200)
    cab_description = models.CharField(length=500)






