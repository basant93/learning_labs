from django.db import models
import datetime

# Create your models here.
class Booking(models.Model):
    booking_id = models.UUIDField(unique= True, editable=False)
    pickup_lat = models.FloatField(null=True,blank=False, verbose_name='latitude')
    pickup_lng = models.FloatField(null=True,blank=False, verbose_name='longitude')
    cab_category_id = models.IntegerField()
    pickup_time= models.DateField(default=datetime.now)
    payment_type_id = models.IntegerField(default=1)
    fare = models.CharField()

