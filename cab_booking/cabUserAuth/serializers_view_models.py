from rest_framework import serializers


class UserResponseDataSerialers(serializers.Serializer):
    """

    """
    id = serializers.IntegerField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    auth_token = serializers.CharField()
    role = serializers.CharField()
    email = serializers.CharField()


class UserResponseSerializer(serializers.Serializer):
    """

    """
    success = serializers.BooleanField()
    error_code = serializers.IntegerField()
    status_code = serializers.CharField()
    data = UserResponseDataSerialers()