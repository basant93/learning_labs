from django.contrib.auth.models import User, Group, Permission
from rest_framework.authtoken.models import Token


class CabUtils(object):



    @staticmethod
    def get_user_by_email(email):
        """

        :return:
        """
        try:
            user_obj = User.objects.get(username=email)
        except:
            user_obj = None

        return user_obj

    @staticmethod
    def get_auth_token(user_id):
        """

        :return:
        """

        token = Token.objects.create(user_id=user_id).key
        return token


    @staticmethod
    def get_role(user_id):
        """

        :return:
        """
        role = User.objects.get(id=user_id).groups.first()

        if role is None:
            return None

        return role.name


