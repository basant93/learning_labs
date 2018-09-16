from cabUtils.utils import CabUtils
from rest_framework.authtoken.models import Token

class UserResponseData(object):
    """

    """

    status = None
    booking_id= None
    message = None

    def __init__(self, cab_booking_obj,google_distance_duration_matrix_api_response):
        self.status = "SUCCESS"
        self.booking_id = cab_booking_obj.cab_booking_id
        self.message = "Cab Booking Successful"
        self.distance = google_distance_duration_matrix_api_response['rows'][0]['elements'][0]['distance']['text']
        self.duration = google_distance_duration_matrix_api_response['rows'][0]['elements'][0]['duration']['text']



    def __str__(self):
        return self.booking_id


class UserPaymentTypeData(object):
    """

    """

    message = None

    def __init__(self):

        self.message = "Payment type added Successful"




    def __str__(self):
        return self.booking_id


