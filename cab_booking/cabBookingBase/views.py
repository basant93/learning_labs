from django.shortcuts import render

# Create your views here.

from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from django.contrib.auth.models import Group, User
from django.db import Error
from . import helper
from . import constants
from cabUtils.utils import CabUtils
from .models import CabBooking, Payment, Cab, cab_category
from math import sin, cos, sqrt, atan2, radians


def calculate_distance(data):
    # approximate radius of earth in km
    R = 6373.0

    # lat1 = radians(52.2296756)
    # lon1 = radians(21.0122287)
    # lat2 = radians(52.406374)
    # lon2 = radians(16.9251681)
    lat1 = data['pickup_lat']
    lon1 = data['pickup_lng']
    lat2 = data['drop_lat']
    lon2 = data['drop_lng']

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    print("Result:", distance)
    print("Should be:", 278.546, "km")
    return distance


@api_view(['POST'])
def create_booking(request):
    """

    :param request:
    :return:
    """
    data = JSONParser().parse(request)
    validation_code = helper.validate_user_data(data)
    user_obj = CabUtils.get_user_by_email(data['email'])

    if (validation_code != constants.get_success_code() or user_obj is None):
        response_error = helper.get_error_response(validation_code)
        return response_error


    # cab_category_obj = cab_category(category='mini', cab_description='this is mini cab', rate_card=10)
    #
    # #cab_category_obj = cab_category.objects.filter(id=1).first()
    # cab_category_obj.save()
    # create_new_cab = Cab()
    # create_new_cab.cab_license_plate_number = 'MH121599'
    # create_new_cab.cab_model_id = cab_category_obj
    # create_new_cab.cab_owner_id = User(id=1)
    # create_new_cab.status = 0
    # create_new_cab.save()
    available_cabs = Cab.objects.filter(status=0).first()

    if(available_cabs is  None):
        response_error = helper.get_error_response(validation_code)
        return response_error

    google_distance_duration_matrix_api_response = helper.get_distance_duration(data)




    if(user_obj is not None ):

        try:
            cab_booking_obj = helper.generate_cab_booking_obj(data,user_obj,available_cabs)
            #cab_booking_obj.save()
            response = helper.get_user_response(cab_booking_obj,google_distance_duration_matrix_api_response)
            return response

        except Error:
            return helper.get_error_response(constants.get_server_error_code())
    else:

        if user_obj.is_active:
            return helper.get_error_response(constants.get_user_exist())
        else:
            user_obj = helper.generate_user_obj(data,encrypted_password,user_obj)
            user_obj.save()
            response = helper.get_user_response(user_obj)
            return response



@api_view(['POST'])
def create_new_payment_type(request):
    """

    :param request:
    :return:
    """
    data = JSONParser().parse(request)

    if (data['payment_id'] == '' or data['payment_name'] =='' ):
        response_error = helper.get_error_response(validation_code)
        return response_error



    if(data is not None ):

        try:
            payment_obj = Payment()
            payment_obj.payment_id = data['payment_id']
            payment_obj.payment_type_name = data['payment_name']
            payment_obj.save()
            response = helper.get_payment_response()
            return response

        except Error:
            return helper.get_error_response(constants.get_server_error_code())


