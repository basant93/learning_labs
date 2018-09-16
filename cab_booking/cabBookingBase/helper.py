

from django.contrib.auth.models import User
import datetime
from rest_framework.response import Response
from .view_models import UserResponseData, UserPaymentTypeData
from rest_framework import status
from .serializers_view_models import UserResponseSerializer, PaymentTypeResponseSerializer
from . import constants
from .models import CabBooking, Cab, Payment, cab_category
import requests
from django.utils.crypto import get_random_string

def validate_user_data(data):
    """

    :param data:
    :return:
    """

    error_code = constants.get_success_code()
    user_id = data['user_id']
    cab_info = data['cab_info']
    pickup_date = data['pickup_date']
    drop_lat = data['drop_lat']
    drop_lng = data['drop_lng']
    pickup_lat = data['pickup_lat']
    pickup_lng = data['pickup_lng']
    category = data['category']
    payment_type = data['payment_type']
    email = data['email']


    if(user_id =='' or cab_info =='' or pickup_date=='' or drop_lat=='' or drop_lng=='' or pickup_lat=='' or pickup_lng=='' or category=='' or payment_type=='' or email==''):
        error_code = constants.get_user_validation_failed_error_code()

    return error_code

def generate_cab_booking_obj(data,user_obj,first_available_cab):
    """

    :param data:
    :param user_obj:
    :return:
    """

    #cab_category_obj = cab_category.objects.filter(category=data['category']).first()

    payment_type_obj = Payment.objects.filter(payment_type_name=data['payment_type']).first()


    cab_booking_obj = CabBooking()
    cab_booking_obj.cab_booking_id = get_random_string(length=15)
    cab_booking_obj.user_id = user_obj.id
    cab_booking_obj.cab_info = first_available_cab
    cab_booking_obj.pickup_date = data["pickup_date"]
    cab_booking_obj.pickup_time_start = datetime.datetime.now()
    cab_booking_obj.drop_lat = data['drop_lat']
    cab_booking_obj.pickup_lat = data['pickup_lat']
    cab_booking_obj.pickup_lng = data['pickup_lng']
    cab_booking_obj.drop_lat = data['drop_lat']
    cab_booking_obj.drop_lng = data['drop_lng']
    cab_booking_obj.status = 1
    cab_booking_obj.payment_type_id = payment_type_obj
    cab_booking_obj.save()
    return cab_booking_obj



def get_user_response(user_obj,google_distance_duration_matrix_api_response):
    """

    :param user_obj:
    :return:
    """
    head_response = Response()
    response_obj = UserResponseData(user_obj,google_distance_duration_matrix_api_response)
    head_response.success = True
    head_response.error_code = 0
    head_response.data = response_obj
    head_response.status_code = status.HTTP_200_OK
    serializer = UserResponseSerializer(head_response)

    return Response(serializer.data)

def get_payment_response():
    """

    :param user_obj:
    :return:
    """
    head_response = Response()
    response_obj = UserPaymentTypeData()
    head_response.success = True
    head_response.error_code = 0
    head_response.data = response_obj
    head_response.status_code = status.HTTP_200_OK
    serializer = PaymentTypeResponseSerializer(head_response)

    return Response(serializer.data)

def get_error_response(error_code):
    """
    This method is used to generate an error response common for all user authentication APIs.
    :param error_code:
    :return: error_response
    """
    error_response = Response()
    error_response.error_code = error_code
    error_response.success = False
    error_response.data = None
    error_response.status_code = status.HTTP_400_BAD_REQUEST
    serializer = UserResponseSerializer(error_response)
    return Response(serializer.data)



def get_distance_duration(data):


    # address = "1600 Amphitheatre Parkway, Mountain View, CA"
    origin = 'Washington,DC'
    destinations = 'New+York+City,NY'
    origins = data['pickup_lat'] +','+data['pickup_lng']
    destinations = data['pickup_lat'] +','+data['pickup_lng']
    api_key = 'KEEPING_EMPTY' #Keep it empty while git commit.
    # api_response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address={0}&key={1}'.format(address, api_key))
    # api_response = requests.get('https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origin={0}&destinations={1}&key={2}'.format(origin, destinations,api_key))
    # api_response = requests.get('https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origin={0}&destinations={1}&key={2}'.format(origin, destinations,api_key))

    api_response = requests.get(
         'https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins=19.445089,74.868980&destinations=18.5567,73.7940&key=AIzaSyCiNWrfTbzFxxle_OkQfl5mwwoKtDG8_MM')
    # api_response_dict = api_response.json()
    #api_response = requests.get(
    #    'https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins={0}&destinations={1}&key={2}'.format(origins,destinations,api_key))
    api_response_dict = api_response.json()

    if api_response_dict['status'] == 'OK':
        distance = api_response_dict['rows'][0]['elements'][0]['distance']['text']
        duration = api_response_dict['rows'][0]['elements'][0]['duration']['text']

        #print('Latitude:', distance)
        #print('Longitude:', duration)
    return api_response_dict