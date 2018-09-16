import re

def get_success_code():
    return 100

def get_user_validation_failed_error_code():
    return 101

def get_password_short_error_code():
    return 102

def get_server_error_code():
    return 103

def get_cab_already_registered_code():
    return 104
# Regex
def get_email_validation_regex():
    return re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")