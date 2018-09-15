from cabUtils.utils import CabUtils
from rest_framework.authtoken.models import Token

class UserResponseData(object):
    """

    """

    id = None
    first_name= None
    last_name = None
    role = None
    email = None
    auth_token = None


    def __init__(self, user_obj):
        self.id = user_obj.id
        self.first_name = user_obj.first_name
        self.last_name = user_obj.last_name
        self.email = user_obj.email
        self.auth_token = CabUtils.get_auth_token(user_obj.id)
        self.role = CabUtils.get_role(user_obj.id)

    def __str__(self):
        return self.first_name




