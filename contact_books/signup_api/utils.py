import re
import logging
import traceback
import secrets

KEY_LENGTH = 32


def check_email_validation(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def generate_api_key():
    response = {"status": "Internal Server Error", "status_code": 500, "message": "Error in creating secret key"}
    try:
        secret_key = secrets.token_urlsafe(KEY_LENGTH)
        response.update({"status": "Success", "status_code": 200, "message": "Secret Key Created Successfully", "secret_key": secret_key})
        return response
    except Exception as e:
        error_message = e.__str__()
        logging.error(error_message)
        traceback.print_exc()
    return response

