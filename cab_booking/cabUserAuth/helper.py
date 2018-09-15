

from django.contrib.auth.models import User
import datetime
from rest_framework.response import Response
from .view_models import UserResponseData
from rest_framework import status
from .serializers_view_models import UserResponseSerializer
from . import constants

def validate_user_data(data):
    """

    :param data:
    :return:
    """

    error_code = constants.get_success_code()
    email = data['email']
    password = data['password']
    name = data['name']

    if(email =='' or password =='' or name=='' or constants.get_email_validation_regex().match(email)):
        error_code = constants.get_user_validation_failed_error_code()
    elif(len(password) < constants.get_password_validation_length()):
        error_code = constants.get_password_short_error_code()
    return error_code

def generate_user_obj(data,password,user_obj):
    """

    :param data:
    :param password:
    :param user_obj:
    :return:
    """
    if(user_obj is None):
        user_obj = User()
    user_obj.email = data["email"]

    user_obj.first_name = data["first_name"]
    user_obj.last_name = data["last_name"]
    user_obj.password = password
    user_obj.is_active = False
    user_obj.date_joined = datetime.datetime.now()
    user_obj.username = data["email"]
    return user_obj


def get_user_response(user_obj):
    """

    :param user_obj:
    :return:
    """
    head_response = Response()
    response_obj = UserResponseData(user_obj)
    head_response.success = True
    head_response.error_code = 0
    head_response.data = response_obj
    head_response.status_code = status.HTTP_200_OK
    serializer = UserResponseSerializer(head_response)

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



