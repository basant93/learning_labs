from django.shortcuts import render

# Create your views here.

from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from django.contrib.auth.models import Group
from django.db import Error
from . import helper
from cabUtils import constants
from cabUtils.utils import CabUtils
from django.contrib.auth.hashers import make_password


@api_view(['POST'])
def register_user(request):
    """

    :param request:
    :return:
    """
    data = JSONParser().parse(request)
    validation_code = helper.validate_user_data(data)

    if validation_code != constants.get_success_code():
        response_error = helper.get_error_response(validation_code)
        #return response_error
    encrypted_password = make_password(data["password"], salt=None, hasher='default')

    user_obj = CabUtils.get_user_by_email(data['email'])
    if(user_obj is None):

        try:
            user_obj = helper.generate_user_obj(data,encrypted_password,None)
            user_obj.save()

            cab_group = Group.objects.get(data['type'])
            user_obj.groups.add(cab_group)

            response = helper.get_user_response(user_obj)
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
















