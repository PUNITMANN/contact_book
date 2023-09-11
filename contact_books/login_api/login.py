import logging
import traceback

from helpers.my_sql_connector import my_sql_execute_query
from login_api.utils import generate_bearer_token


def log_in(data):
    response = {"status": "Internal Server Error", "status_code": 500, "message": "Some Internal Error Occurred"}
    try:
        email = data.get("email", "")
        password = data.get("password", "")

        if not email:
            response.update({"status": "Bad Request", "status_code": 400, "message": "Email must not be empty"})
            return response
        if not password:
            response.update(
                {"status": "Bad Request", "status_code": 400, "message": "Both Password must not be empty"})
            return response

        query = "select * from auth_user;"
        results, status_code = my_sql_execute_query(query)
        if status_code == 500:
            return response
        if status_code == 200:
            email_exists = any(item[1] == email for item in results)
            password_exists = any(item[2] == password for item in results)
            if not email_exists:
                response.update({"status": "Bad Request", "status_code": 400, "message": "Invalid Email"})
                return response
            if not password_exists:
                response.update({"status": "Bad Request", "status_code": 400, "message": "Invalid Password"})
                return response

        token = generate_bearer_token(email)
        if token.get("status_code") == 500:
            response.update({"message": token.get("message")})
            return response
        bearer_token = token.get("token")
        x_api_key = token.get("xapi")

        query2 = f"UPDATE auth_user SET access_token='{bearer_token}', last_login=NOW() where email = '{email}'"
        results, status_code = my_sql_execute_query(query2)
        if status_code == 500:
            return response
        response.update({"status": "success", "status_code": 200, "message": "Login Successfully", "Bearer_token": bearer_token, "x_api_key": x_api_key})
        return response

    except Exception as e:
        error_message = e.__str__()
        logging.error(error_message)
        traceback.print_exc()
        return response

