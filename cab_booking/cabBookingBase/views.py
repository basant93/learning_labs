from django.shortcuts import render

# Create your views here.

from django.contrib.auth.models import Group, User
from django.conf import settings
from rest_framework.authtoken.models import Token
from django.db import Error
from . import helper
from . import constants
from cabUtils.utils import CabUtils
from .models import CabBooking, Payment, Cab, cab_category,PaymentDetails, Driver
from math import sin, cos, sqrt, atan2, radians
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny


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
#@permission_classes((AllowAny,))
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

    #There are charges for each api request. Use it only when necessary.
    google_distance_duration_matrix_api_response = helper.get_distance_duration(data)

    cab_rate = cab_category.objects.filter(category=data['category']).first()
    distance = 30
    duration = 4
    origin = "baner"
    destination = "koregaon Park"
    cab_fare = 30 * cab_rate.rate_card + 4 * 4

    #fare = (google_distance_duration_matrix_api_response['rows'][0]['elements'][0]['distance']['text']) *


    if(user_obj is not None ):

        try:
            generate_booking_id = helper.generate_cab_booking_obj(data,user_obj,available_cabs)
            #cab_booking_obj.save()
            #cab_booking_obj = CabBooking.objects.get(cab_booking_id=cab_booking_obj.cab_booking_id)
            cab_booking_obj = CabBooking.objects.filter(cab_booking_id=generate_booking_id).first()

            payment_details_obj = PaymentDetails(payment_type = data['payment_type'], fare=cab_fare, user=user_obj,
                                                 payment_booking=cab_booking_obj, origin=origin,destination=destination)
            payment_details_obj.save()
            available_driver_obj = Cab.objects.filter(status=0).first()
            driver_obj = Driver.objects.get(cab_driver=available_driver_obj)
            driver_obj.driver_booking = cab_booking_obj
            driver_obj.save()

            #cab_booking_obj = helper.generate_cab_payment_details_obj(data,user_obj,cab_booking_obj)
            response = helper.get_user_response(cab_booking_obj,google_distance_duration_matrix_api_response)
            return response

        except Error:
            return helper.get_error_response(constants.get_server_error_code())




@api_view(['POST'])
def create_new_payment_type(request):
    """

    :param request:
    :return:
    """
    data = JSONParser().parse(request)

    if (data['payment_id'] == '' or data['payment_name'] =='' ):
        response_error = helper.get_error_response(constants.get_user_validation_failed_error_code())
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


@api_view(['POST'])
def create_new_cab(request):
    """

    :param request:
    :return:
    """
    data = JSONParser().parse(request)
    # #token = request.META.get('Authorization', None)
    # token = request.META.get('Authorization', None)
    # check_valid_token = Token.objects.filter(key=token).exists()
    # if(check_valid_token is  False):
    #     response_error = helper.get_error_response(constants.get_user_validation_failed_error_code())
    #     return response_error


    user_obj = CabUtils.get_user_by_email(data['user_mail'])

    if (data['license_plate_number'] == '' or data['category'] =='' or data['rate_per_km'] == '' or data['user_mail'] =='' or user_obj is None):
        response_error = helper.get_error_response(constants.get_user_validation_failed_error_code())
        return response_error

    check_cab_registrations = Cab.objects.filter(cab_license_plate_number = data['license_plate_number']).exists()

    if(check_cab_registrations is False ):

        try:
            cab_obj = helper.generate_cab_obj(data,user_obj)
            cab_obj.save()
            response = helper.get_new_cab_response()
            return response

        except Error:
            return helper.get_error_response(constants.get_server_error_code())
    elif(check_cab_registrations is True):
        return helper.get_error_response(constants.get_cab_already_registered_code())


@api_view(['POST'])
def fetch_travel_history(request):
    """

    :param request:
    :return:
    """
    data = JSONParser().parse(request)

    user_obj = CabUtils.get_user_by_email(data['user_mail'])

    if ( user_obj is None):
        response_error = helper.get_error_response(constants.get_user_validation_failed_error_code())
        return response_error

    all_cab_booking = CabBooking.objects.filter(user__email = data['user_mail'])

    if(len(all_cab_booking) >0  ):

        try:
            cab_obj = helper.generate_cab_obj(data,user_obj)
            cab_obj.save()
            response = helper.get_new_cab_response()
            return response

        except Error:
            return helper.get_error_response(constants.get_server_error_code())
    elif(len(all_cab_booking) ==0):
        return helper.get_error_response(constants.get_cab_already_registered_code())
