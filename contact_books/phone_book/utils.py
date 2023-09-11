import phonenumbers
from phonenumbers.phonenumberutil import NumberParseException, PhoneNumberType

NAME_LIMIT = 41
ADDRESS_LIMIT = 150
NOTES_LIMIT = 1000

def validate_phonenumber(phone_number):
    is_valid_number = False
    message = "Not a valid mobile number"
    try:
        parsed_number = phonenumbers.parse(phone_number, None)
        number_type_result = phonenumbers.number_type(parsed_number)

        if number_type_result == PhoneNumberType.MOBILE:
            is_valid_number = True
            message = "valid mobile number"
        else:
            is_valid_number = False
            message = "Not a valid mobile number"

    except NumberParseException as ex:
        message = "Missing or invalid default region"

    if not is_valid_number:
        if len(phone_number) == 10:
            is_valid_number = True
            message = "valid mobile number"
        elif len(phone_number) == 11 and phone_number[0] == "0":
            is_valid_number = True
            message = "valid mobile number"

    return is_valid_number, message

def validate_alternative_phonenumber(alternate_phone_numbers):
    for number in alternate_phone_numbers:
        is_valid, message = validate_phonenumber(number)
        if not is_valid:
            response = {"status": "Bad Request", "status_code": 400, "message": message, "invalid_number": number}
            return response
    return {"status": "success", "status_code": 200, "message": "valid alternative numbers"}


def params_validator(data):
    is_valid = True
    message = "Valid Parameter"

    name = data.get("name", "")
    address = data.get("address", "")
    notes = data.get("notes", "")

    if len(name) > NAME_LIMIT:
        is_valid = False
        message = "Name Length must be less than 40"

    if len(address) > ADDRESS_LIMIT:
        is_valid = False
        message = f"Address Length must be less than {ADDRESS_LIMIT}"

    if len(notes) > NOTES_LIMIT:
        is_valid = False
        message = f"Notes Length must be less than {NOTES_LIMIT}"

    return is_valid, message

