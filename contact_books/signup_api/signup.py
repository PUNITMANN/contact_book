import traceback
import logging
from datetime import datetime

from helpers.my_sql_connector import my_sql_execute_query
from signup_api.utils import check_email_validation, generate_api_key


def sign_up(data):
    response = {"status": "Internal Server Error", "status_code": 500, "message": "Some Internal Error Occurred"}
    try:
        email = data.get("email", "")
        password = data.get("password", "")
        re_enter_password = data.get("re_enter_password", "")

        if not email:
            response.update({"status": "Bad Request", "status_code": 400, "message": "Email must not be empty"})
            return response
        if not password or not re_enter_password:
            response.update({"status": "Bad Request", "status_code": 400, "message": "Both Password must not be empty"})
            return response

        if password != re_enter_password:
            response.update({"status": "Bad Request", "status_code": 400, "message": "Both Password must be same"})
            return response

        email_valid = check_email_validation(email)
        if not email_valid:
            response.update({"status": "Bad Request", "status_code": 400, "message": "Invalid Email Format"})
            return response

        query = "select * from auth_user;"
        results, status_code = my_sql_execute_query(query)
        if status_code == 500:
            return response
        if status_code == 200:
            email_exists = any(item[1] == email for item in results)
            if email_exists:
                response.update({"status": "Bad Request", "status_code": 400, "message": "Email Already Exists"})
                return response

        result = generate_api_key()
        if result.get("status_code") == 500:
            return result
        x_api_key = result.get("secret_key")
        query2 = f"insert into auth_user (email, password, created_at, x_api_key) VALUES ('{email}', '{password}', NOW(), '{x_api_key}');"
        results, status_code = my_sql_execute_query(query2)
        if status_code == 500:
            response.update({"status": "Bad Request", "status_code": 400, "message": "Error in Inserting Data into Database"})
            return response
        if status_code == 200:
            response.update({"status": "Success", "status_code": 200, "message": f"User with email {email} signed up successfully", "x_api_key": x_api_key})
            return response

    except Exception as e:
        error_message = e.__str__()
        logging.error(error_message)
        traceback.print_exc()
        return response
