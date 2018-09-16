from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

app_name = 'cabBookingBase'
urlpatterns = [
    url(r'^create/booking', views.create_booking),
    url(r'^create/payment/type', views.create_new_payment_type),
    url(r'^create/cab', views.create_new_cab)
]

urlpatterns = format_suffix_patterns(urlpatterns)