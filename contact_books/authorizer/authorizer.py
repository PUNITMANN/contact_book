import jwt
import requests
from functools import wraps
from datetime import datetime

from login_api.utils import PRIVATE_KEY


def validate_token(token):
    try:
        payload = jwt.decode(token, PRIVATE_KEY, algorithms=["HS256"])
        if datetime.utcnow() > datetime.fromtimestamp(payload["exp"]):
            return False
        return payload
    except jwt.ExpiredSignatureError as e:
        return False
    except jwt.DecodeError as e:
        return False


def token_required(func):
    @wraps(func)
    async def middleware(request, *args, **kwargs):
        token = request.headers.get("Authorization", "")
        x_api_key = request.headers.get("x-api-key", "")

        if not token or not x_api_key:
            return {"status": "Unauthorized", "status_code": 401, "message": "Token or x-api-key missing"}
        payload = validate_token(token)
        if not payload:
            return {"status": "Unauthorized", "status_code": 401, "message": "Invalid or expired token"}

        request.state.user_id = payload
        return await func(request, *args, **kwargs)
    return middleware

