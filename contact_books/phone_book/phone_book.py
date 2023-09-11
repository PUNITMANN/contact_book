import logging
import traceback
from datetime import datetime

from helpers.mongodb_connector import mongodb_query_execute
from phone_book.utils import validate_phonenumber, params_validator
from signup_api.utils import check_email_validation


def phone_book(data, user_id):
    response = {"status": "Internal Server Error", "status_code": 500, "message": "Some Internal Error Occurred"}
    try:
        phone_number = data.get("phone_number", "")
        name = data.get("name", "")
        address = data.get("address", "")
        alternate_phone_numbers = data.get("alternate_phone_number", "")
        email = data.get("email", "")
        notes = data.get("notes", "")
        created_at = datetime.now()

        if not user_id:
            response.update({"status": "Unauthorized", "status_code": 401, "message": "User Id must not be Empty"})
            return response

        if not phone_number:
            response.update({"status": "Bad Request", "status_code": 400, "message": "Phone Number must not be Empty"})
            return response
        if not name:
            response.update({"status": "Bad Request", "status_code": 400, "message": "Name must not be Empty"})
            return response

        is_valid, message = validate_phonenumber(phone_number)
        if not is_valid:
            response.update({"status": "Bad Request", "status_code": 400, "message": message + " in Phone Number"})
            return response

        result = mongodb_query_execute("phone_book_collection", "find_one", filter={"phone_number": phone_number, "user_id": user_id})
        if result:
            response.update({"status": "Bad Request", "status_code": 400, "message": "Phone Number is Already Present"})
            return response

        is_valid, message = params_validator(data)
        if not is_valid:
            response.update({"status": "Bad Request", "status_code": 400, "message": message})
            return response

        email_valid = check_email_validation(email)
        if not email_valid:
            response.update({"status": "Bad Request", "status_code": 400, "message": "Invalid Email Format"})
            return response

        is_valid, message = validate_phonenumber(alternate_phone_numbers)
        if not is_valid:
            response.update({"status": "Bad Request", "status_code": 400, "message": message+" in Alternate Phone Number"})
            return response

        phone_book_data = {
            "user_id": user_id,
            "phone_number": phone_number,
            "email": email,
            "name": name,
            "address": address,
            "alternate_phone_number": alternate_phone_numbers,
            "notes": notes,
            "created_at": created_at
        }

        result = mongodb_query_execute("phone_book_collection", "insert_one", data=phone_book_data)
        is_inserted_id = result.inserted_id
        if not is_inserted_id:
            response.update({"status": "Bad Request", "status_code": 400, "message": "Error in Logging the phone number"})
        response.update({"status": "Success", "status_code": 200, "message": "Phone Number Logged Successfully"})
        return response
    except Exception as e:
        error_message = e.__str__()
        logging.error(error_message)
        traceback.print_exc()
    return response


def get_phone_book(user_id):
    response = {"status": "Internal Server Error", "status_code": 500, "message": "Some Internal Error Occurred"}
    try:
        data = []
        if not user_id:
            response.update({"status": "Unauthorized", "status_code": 401, "message": "User Id must not be Empty"})
            return response
        filter = {"user_id": user_id}
        results = mongodb_query_execute("phone_book_collection", "find", filter=filter, projection={"_id": 0})
        for result in results:
            data.append(result)
        response.update({"status": "Success", "status_code": 200, "message": "Phone Logs fetched Successfully", "data": data})
        return response
    except Exception as e:
        error_message = e.__str__()
        logging.error(error_message)
        traceback.print_exc()
    return response


def update_phone_book(data, user_id, phone_number):
    response = {"status": "Internal Server Error", "status_code": 500, "message": "Some Internal Error Occurred"}
    try:
        name = data.get("name", "")
        address = data.get("address", "")
        alternate_phone_numbers = data.get("alternate_phone_number", "")
        email = data.get("email", "")
        notes = data.get("notes", "")
        updated_at = datetime.now()

        if not user_id:
            response.update({"status": "Unauthorized", "status_code": 401, "message": "User Id must not be Empty"})
            return response
        if not phone_number:
            response.update({"status": "Bad Request", "status_code": 400, "message": "Phone Number must not be Empty"})
            return response
        if not name:
            response.update({"status": "Bad Request", "status_code": 400, "message": "Name must not be Empty"})
            return response

        is_valid, message = validate_phonenumber(phone_number)
        if not is_valid:
            response.update({"status": "Bad Request", "status_code": 400, "message": message + " in Phone Number"})
            return response
        filter = {"phone_number": phone_number, "user_id": user_id}
        result = mongodb_query_execute("phone_book_collection", "find_one", filter=filter)
        if result is None:
            response.update({"status": "Bad Request", "status_code": 400, "message": "Phone Number is Not Present"})
            return response

        is_valid, message = params_validator(data)
        if not is_valid:
            response.update({"status": "Bad Request", "status_code": 400, "message": message})
            return response

        if email:
            email_valid = check_email_validation(email)
            if not email_valid:
                response.update({"status": "Bad Request", "status_code": 400, "message": "Invalid Email Format"})
                return response

        if alternate_phone_numbers:
            is_valid, message = validate_phonenumber(alternate_phone_numbers)
            if not is_valid:
                response.update({"status": "Bad Request", "status_code": 400, "message": message+" in Alternate Phone Number"})
                return response

        phone_book_data = {
            "user_id": user_id,
            "phone_number": phone_number,
            "email": email,
            "name": name,
            "address": address,
            "alternate_phone_number": alternate_phone_numbers,
            "notes": notes,
            "updated_at": updated_at
        }
        update_data = {"$set": phone_book_data}
        filter = {"phone_number": phone_number, "user_id": user_id}
        result = mongodb_query_execute("phone_book_collection", "update_one", filter=filter, update_data=update_data)
        is_acknowladged = result.acknowledged
        if not is_acknowladged:
            response.update({"status": "Bad Request", "status_code": 400, "message": "Error in Updating the phone number"})
        response.update({"status": "Success", "status_code": 200, "message": "Phone Number Updated Successfully"})
        return response
    except Exception as e:
        error_message = e.__str__()
        logging.error(error_message)
        traceback.print_exc()
    return response


def delete_phone_log(user_id, phone_number):
    response = {"status": "Internal Server Error", "status_code": 500, "message": "Some Internal Error Occurred"}
    try:
        if not user_id:
            response.update({"status": "Unauthorized", "status_code": 401, "message": "User Id must not be Empty"})
            return response
        if not phone_number:
            response.update({"status": "Bad Request", "status_code": 400, "message": "Phone Number must not be Empty"})
            return response
        filter = {"phone_number": phone_number, "user_id": user_id}
        result = mongodb_query_execute("phone_book_collection", "find_one", filter=filter)
        if not result:
            response.update({"status": "Bad Request", "status_code": 400, "message": "Phone Number is Not Present"})
            return response
        result = mongodb_query_execute("phone_book_collection", "delete_one", filter=filter)
        if not result.acknowledged:
            response.update({"status": "Bad Request", "status_code": 400, "message": f"Error in Deleting Phone Log {phone_number}"})
            return response

        response.update(
            {"status": "Success", "status_code": 200, "message": f"Phone Log {phone_number} Deleted Successfully"})
        return response

    except Exception as e:
        error_message = e.__str__()
        logging.error(error_message)
        traceback.print_exc()
    return response
