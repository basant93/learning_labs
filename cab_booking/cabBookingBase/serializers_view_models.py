from rest_framework import serializers


class UserResponseDataSerialers(serializers.Serializer):
    """

    """
    status = serializers.CharField()
    booking_id = serializers.CharField()
    message = serializers.CharField()
    distance = serializers.CharField()
    duration = serializers.CharField()



class UserResponseSerializer(serializers.Serializer):
    """

    """
    success = serializers.BooleanField()
    error_code = serializers.IntegerField()
    status_code = serializers.CharField()
    data = UserResponseDataSerialers()







class PaymentTypeDataResponseDataSerialers(serializers.Serializer):
    """

    """

    message = serializers.CharField()




class PaymentTypeResponseSerializer(serializers.Serializer):
    """

    """
    success = serializers.BooleanField()
    error_code = serializers.IntegerField()
    status_code = serializers.CharField()
    data = PaymentTypeDataResponseDataSerialers()


class NewCabeDataResponseDataSerialers(serializers.Serializer):
    """

    """

    message = serializers.CharField()




class NewCabResponseSerializer(serializers.Serializer):
    """

    """
    success = serializers.BooleanField()
    error_code = serializers.IntegerField()
    status_code = serializers.CharField()
    data = NewCabeDataResponseDataSerialers()